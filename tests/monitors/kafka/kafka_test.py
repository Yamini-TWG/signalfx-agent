import os
import pytest

from tests.kubernetes.utils import (
    run_k8s_monitors_test,
    get_metrics_from_doc,
    get_dims_from_doc,
)

pytestmark = [pytest.mark.collectd, pytest.mark.kafka, pytest.mark.monitor_with_endpoints]


@pytest.mark.k8s
@pytest.mark.kubernetes
def test_kafka_in_k8s(agent_image, minikube, k8s_observer, k8s_test_timeout):
    monitors = [
        {"type": "collectd/kafka",
         "discoveryRule": 'container_image =~ "kafka" && private_port == 7302',
         "serviceURL": 'service:jmx:rmi:///jndi/rmi://{{.Host}}:{{.Port}}/jmxrmi',
         "username": "testuser", "password": "testing123"},
    ]
    yamls = [os.path.join(os.path.dirname(os.path.realpath(__file__)), y) for y in ["kafka-configmap.yaml", "kafka.yaml"]]
    run_k8s_monitors_test(
        agent_image,
        minikube,
        monitors,
        yamls=yamls,
        observer=k8s_observer,
        expected_metrics=get_metrics_from_doc("collectd-kafka.md"),
        expected_dims=get_dims_from_doc("collectd-kafka.md"),
        test_timeout=k8s_test_timeout)

