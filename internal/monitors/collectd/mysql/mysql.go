package mysql

//go:generate collectd-template-to-go mysql.tmpl

import (
	"errors"

	"github.com/signalfx/signalfx-agent/internal/core/config"
	"github.com/signalfx/signalfx-agent/internal/monitors"
	"github.com/signalfx/signalfx-agent/internal/monitors/collectd"
)

const monitorType = "collectd/mysql"

func init() {
	monitors.Register(monitorType, func() interface{} {
		return &Monitor{
			*collectd.NewMonitorCore(CollectdTemplate),
		}
	}, &Config{})
}

// Config is the monitor-specific config with the generic config embedded
type Config struct {
	config.MonitorConfig `yaml:",inline" acceptsEndpoints:"true"`

	Host      string `yaml:"host" validate:"required"`
	Port      uint16 `yaml:"port" validate:"required"`
	Name      string `yaml:"name"`
	Databases []struct {
		Name     string `yaml:"name"`
		Username string `yaml:"username"`
		Password string `yaml:"password" neverLog:"true"`
	} `yaml:"databases" required:"true"`
	// These credentials serve as defaults for all databases if not overridden
	Username   string `yaml:"username"`
	Password   string `yaml:"password" neverLog:"true"`
	ReportHost bool   `yaml:"reportHost"`
}

// Validate will check the config for correctness.
func (c *Config) Validate() error {
	if len(c.Databases) == 0 {
		return errors.New("You must specify at least one database for MySQL")
	}

	for _, db := range c.Databases {
		if db.Username == "" && c.Username == "" {
			return errors.New("Username is required for MySQL monitoring")
		}
	}
	return nil
}

// Monitor is the main type that represents the monitor
type Monitor struct {
	collectd.MonitorCore
}

// Configure configures and runs the plugin in collectd
func (am *Monitor) Configure(conf *Config) error {
	return am.SetConfigurationAndRun(conf)
}