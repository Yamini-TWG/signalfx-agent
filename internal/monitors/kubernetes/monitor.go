// Package kubernetes contains a Kubernetes monitor.
//
// This plugin collects high level metrics about a K8s cluster and sends them
// to SignalFx.  The basic technique is to pull data from the K8s API and keep
// up-to-date copies of datapoints for each metric that we collect and then
// ship them off at the end of each reporting interval.  The K8s streaming
// watch API is used to effeciently maintain the state between read intervals
// (see `clusterstate.go`).
//
// This plugin should only be run at one place in the cluster, or else metrics
// would be duplicated.  This plugin supports two ways of ensuring that:
//
// 1) With the default configuration, this plugin will watch the current list
// of our agent pods, and if and only if it is the first pod in the list,
// sorted alphabetically by pod name ascending, it will be a reporter. Each
// instance of the agent will check upon each reporting interval whether it is
// the first such pod and begin reporting if it finds that it has become the
// reporter.  This method requires one long-running connection to the K8s API
// server per node (assuming the agent is running on all nodes).
//
// 2) You can simply pass a config flag `alwaysClusterReporter` with value of
// `true` to this plugin and it will always report cluster metrics.  This
// method uses less cluster resources (e.g. network sockets, watches on the api
// server) but requires special case configuration for a single agent in the
// cluster, which may be more error prone.
//
// This plugin requires read-only access to the K8s API.
package kubernetes

import (
	"os"
	"reflect"
	"sort"
	"time"

	"k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"

	"github.com/pkg/errors"
	log "github.com/sirupsen/logrus"

	"github.com/signalfx/signalfx-agent/internal/core/common/dpmeta"
	"github.com/signalfx/signalfx-agent/internal/core/common/kubernetes"
	"github.com/signalfx/signalfx-agent/internal/core/config"
	"github.com/signalfx/signalfx-agent/internal/monitors"
	"github.com/signalfx/signalfx-agent/internal/monitors/kubernetes/metrics"
	"github.com/signalfx/signalfx-agent/internal/monitors/types"

	"sync"
)

const (
	monitorType = "kubernetes-cluster"
)

var logger = log.WithFields(log.Fields{"monitorType": monitorType})

// Config for the K8s monitor
type Config struct {
	config.MonitorConfig
	AlwaysClusterReporter bool                  `yaml:"alwaysClusterReporter"`
	KubernetesAPI         *kubernetes.APIConfig `yaml:"kubernetesAPI" default:"{}"`
}

// Validate the k8s-specific config
func (c *Config) Validate() error {
	return c.KubernetesAPI.Validate()
}

// Monitor for K8s Cluster Metrics.  Also handles syncing certain properties
// about pods.
type Monitor struct {
	config      *Config
	lock        sync.Mutex
	Output      types.Output
	thisPodName string
	// Since most datapoints will stay the same or only slightly different
	// across reporting intervals, reuse them
	datapointCache *metrics.DatapointCache
	clusterState   *ClusterState
	stop           chan struct{}
}

func init() {
	monitors.Register(monitorType, func() interface{} { return &Monitor{} }, &Config{})
}

// Configure is called by the plugin framework when configuration changes
func (m *Monitor) Configure(config *Config) error {
	m.lock.Lock()
	defer m.lock.Unlock()

	// There is a bug/limitation in the k8s go client's Controller where
	// goroutines are leaked even when using the stop channel properly.  So we
	// should avoid going through a shutdown/startup cycle here if nothing is
	// different in the config.
	// See https://github.com/kubernetes/client-go/blob/v2.0.0/tools/cache/controller.go#L125
	if reflect.DeepEqual(config, m.config) {
		return nil
	}

	m.config = config

	m.stopIfRunning()

	k8sClient, err := kubernetes.MakeClient(config.KubernetesAPI)
	if err != nil {
		return errors.Wrapf(err, "Could not create K8s API client")
	}

	// We need to know the pod name if we aren't always reporting
	if !config.AlwaysClusterReporter {
		var ok bool
		m.thisPodName, ok = os.LookupEnv("MY_POD_NAME")
		if !ok {
			return errors.New("This pod's name is not known! Please inject the envvar MY_POD_NAME " +
				"via a config fieldRef in your K8s agent resource config")
		}
	}

	m.datapointCache = metrics.NewDatapointCache()

	m.clusterState = newClusterState(k8sClient)
	m.clusterState.ChangeFunc = func(oldObj, newObj runtime.Object) {
		m.datapointCache.HandleChange(oldObj, newObj)
	}

	m.Start(config.IntervalSeconds)

	return nil
}

// Start starts syncing resources and sending datapoints to ingest
func (m *Monitor) Start(intervalSeconds int) error {
	m.clusterState.StartSyncing(&v1.Pod{})

	m.stop = make(chan struct{})
	ticker := time.NewTicker(time.Second * time.Duration(intervalSeconds))

	go func() {
		defer ticker.Stop()

		for {
			select {
			case <-m.stop:
				return
			case <-ticker.C:
				if m.isReporter() {
					log.Debugf("This agent is a K8s cluster reporter")
					m.clusterState.EnsureAllStarted()
					m.sendLatestDatapoints()
					m.sendLatestProps()
				}
			}
		}
	}()

	return nil
}

// Synchonously send all of the cached datapoints to ingest
func (m *Monitor) sendLatestDatapoints() {
	dps := m.datapointCache.AllDatapoints()

	now := time.Now()
	for i := range dps {
		dps[i].Timestamp = now
		dps[i].Meta[dpmeta.NotHostSpecificMeta] = true
		m.Output.SendDatapoint(dps[i])
	}
}

func (m *Monitor) sendLatestProps() {
	dimProps := m.datapointCache.AllDimProperties()

	for i := range dimProps {
		m.Output.SendDimensionProps(dimProps[i])
	}
}

// We only need one agent to report high-level K8s metrics so we need to
// deterministically choose one without the agents being able to talk to one
// another (for simplified setup).  About the simplest way to do that is to
// have it be the agent with the pod name that is first when all of the names
// are sorted ascending.
func (m *Monitor) isReporter() bool {
	if m.config.AlwaysClusterReporter {
		return true
	}

	agentPods, err := m.clusterState.GetAgentPods()
	if err != nil {
		log.WithError(err).Error("Unexpected error getting agent pods")
		return false
	}

	// This shouldn't really happen, but don't blow up if it does
	if len(agentPods) == 0 {
		return false
	}

	sort.Slice(agentPods, func(i, j int) bool {
		return agentPods[i].Name < agentPods[j].Name
	})

	return agentPods[0].Name == m.thisPodName
}

func (m *Monitor) stopIfRunning() {
	if m.stop != nil {
		m.stop <- struct{}{}
	}
	if m.clusterState != nil {
		m.clusterState.Stop()
	}
}

// Shutdown halts everything that is syncing
func (m *Monitor) Shutdown() {
	m.lock.Lock()
	defer m.lock.Unlock()

	m.stopIfRunning()
	m.config = nil
}