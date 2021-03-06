from tests.kubernetes.utils import get_metrics_from_doc, get_dims_from_doc

# list of monitor definitions
# the monitor should be a YAML-based dictionary which will be used for the signalfx-agent agent.yaml configuration
MONITORS_WITHOUT_ENDPOINTS = [
    {"type": "cadvisor"},
    {"type": "collectd/cpu"},
    {"type": "collectd/cpufreq"},
    {"type": "collectd/custom"},
    {"type": "collectd/df",
     "hostFSPath": "/hostfs"},
    {"type": "collectd/disk"},
    {"type": "collectd/docker",
     "dockerURL": "unix:///var/run/docker.sock",
     "collectNetworkStats": True},
    {"type": "collectd/interface"},
    {"type": "collectd/load"},
    {"type": "collectd/memory"},
    {"type": "collectd/processes",
     "procFSPath": "/hostfs/proc",
     "collectContextSwitch": True,
     "processMatch": {"docker": "docker.*"}},
    {"type": "collectd/protocols"},
    {"type": "collectd/signalfx-metadata",
     "procFSPath": "/hostfs/proc", "etcPath": "/hostfs/etc", "persistencePath": "/var/run/signalfx-agent"},
    {"type": "collectd/statsd",
     "listenAddress": "127.0.0.1",
     "listenPort": 8125,
     "counterSum": True,
     "deleteSets": True,
     "deleteCounters": True,
     "deleteTimers": True,
     "deleteGauges": True},
    {"type": "collectd/uptime"},
    {"type": "collectd/vmem"},
    {"type": "docker-container-stats"},
    {"type": "internal-metrics"},
    {"type": "kubelet-stats",
     "kubeletAPI": {"skipVerify": True, "authType": "serviceAccount"}},
    {"type": "kubernetes-cluster",
     "kubernetesAPI": {"authType": "serviceAccount"}},
    {"type": "kubernetes-events",
     "kubernetesAPI": {"authType": "serviceAccount"}},
    {"type": "kubernetes-volumes",
     "kubeletAPI": {"skipVerify": True, "authType": "serviceAccount"}},
]

# list of tuples containing the monitor definition and list of K8S yamls to deploy
# the monitor should be a YAML-based dictionary which will be used for the signalfx-agent agent.yaml configuration
MONITORS_WITH_ENDPOINTS = [
    ({"type": "collectd/activemq",
      "discoveryRule": 'container_image =~ "activemq" && private_port == 1099',
      "serviceURL": 'service:jmx:rmi:///jndi/rmi://{{.Host}}:{{.Port}}/jmxrmi',
      "username": "testuser", "password": "testing123"},
     ["activemq.yaml"]),
    ({"type": "collectd/apache",
      "discoveryRule": 'container_image =~ "httpd" && private_port == 80',
      "url": 'http://{{.Host}}:{{.Port}}/mod_status?auto',
      "username": "testuser", "password": "testing123"},
     ["apache-configmap.yaml", "apache.yaml"]),
    ({"type": "collectd/cassandra",
      "discoveryRule": 'container_image =~ "cassandra" && private_port == 7199',
      "username": "testuser", "password": "testing123"},
     ["cassandra-configmap.yaml", "cassandra.yaml"]),
    ({"type": "collectd/consul",
      "discoveryRule": 'container_image =~ "consul" && private_port == 8500',
      "aclToken": "testing123",
      "signalFxAccessToken": "testing123",
      "enhancedMetrics": True},
     ["consul.yaml"]),
    ({"type": "collectd/elasticsearch",
      "discoveryRule": 'container_image =~ "elasticsearch" && private_port == 9200',
      "username": "testuser", "password": "testing123"},
     ["elasticsearch.yaml"]),
    ({"type": "collectd/etcd",
      "discoveryRule": 'container_image =~ "etcd" && private_port == 2379',
      "clusterName": "etcd-cluster",
      "skipSSLValidation": True,
      "enhancedMetrics": True},
     ["etcd.yaml"]),
    ({"type": "collectd/genericjmx",
      "discoveryRule": 'container_image =~ "activemq" && private_port == 1099',
      "serviceURL": 'service:jmx:rmi:///jndi/rmi://{{.Host}}:{{.Port}}/jmxrmi',
      "username": "testuser", "password": "testing123"},
     ["activemq.yaml"]),
    ({"type": "collectd/haproxy",
      "discoveryRule": 'container_image =~ "haproxy" && private_port == 9000',
      "enhancedMetrics": True},
     ["haproxy-configmap.yaml", "haproxy.yaml"]),
    ({"type": "collectd/health-checker",
      "discoveryRule": 'container_image =~ "json-server" && private_port == 80',
      "url": 'http://{{.Host}}:{{.Port}}/health',
      "jsonKey": "status",
      "jsonVal": "ok"},
     ["health-checker-configmap.yaml", "health-checker.yaml"]),
    ({"type": "collectd/kafka",
      "discoveryRule": 'container_image =~ "kafka" && private_port == 7302',
      "serviceURL": 'service:jmx:rmi:///jndi/rmi://{{.Host}}:{{.Port}}/jmxrmi',
      "username": "testuser", "password": "testing123"},
     ["kafka-configmap.yaml", "kafka.yaml"]),
    ({"type": "collectd/marathon",
      "discoveryRule": 'container_image =~ "marathon" && private_port == 8080',
      "username": "testuser", "password": "testing123"},
     ["marathon.yaml"]),
    ({"type": "collectd/memcached",
      "discoveryRule": 'container_image =~ "memcached" && private_port == 11211'},
     ["memcached.yaml"]),
    ({"type": "collectd/mongodb",
      "discoveryRule": 'container_image =~ "mongo" && private_port == 27017',
      "databases": ["admin"],
      "username": "testuser", "password": "testing123"},
     ["mongodb.yaml"]),
    ({"type": "collectd/mysql",
      "discoveryRule": 'container_image =~ "mysql" && private_port == 3306',
      "databases": [{"name": "testdb", "username": "root", "password": "testing123"}],
      "username": "root", "password": "testing123"},
     ["mysql.yaml"]),
    ({"type": "collectd/nginx",
      "discoveryRule": 'container_image =~ "nginx" && private_port == 80',
      "url": 'http://{{.Host}}:{{.Port}}/nginx_status',
      "username": "testuser", "password": "testing123"},
     ["nginx-configmap.yaml", "nginx.yaml"]),
    ({"type": "collectd/rabbitmq",
      "discoveryRule": 'container_image =~ "rabbitmq" && private_port == 15672',
      "collectChannels": True,
      "collectConnections": True,
      "collectExchanges": True,
      "collectNodes": True,
      "collectQueues": True,
      "username": "testuser", "password": "testing123"},
     ["rabbitmq.yaml"]),
    ({"type": "collectd/redis",
      "discoveryRule": 'container_image =~ "redis" && private_port == 6379'},
     ["redis.yaml"]),
    ({"type": "collectd/spark",
      "discoveryRule": 'container_image =~ "spark" && private_port == 8080',
      "clusterType": "Standalone",
      "isMaster": True,
      "collectApplicationMetrics": True,
      "enhancedMetrics": True},
     ["spark.yaml"]),
    ({"type": "collectd/zookeeper",
      "discoveryRule": 'container_image =~ "zookeeper" && private_port == 2181'},
     ["zookeeper.yaml"]),
    ({"type": "prometheus-exporter",
      "discoveryRule": 'container_image =~ "prometheus" && private_port == 9090',
      "useHTTPS": False,
      "skipVerify": True,
      "metricPath": "/metrics"},
     ["prometheus.yaml"]),
]

