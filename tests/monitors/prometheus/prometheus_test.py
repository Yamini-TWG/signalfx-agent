import os
import pytest

from tests.kubernetes.utils import (
    run_k8s_monitors_test,
    get_metrics_from_doc,
    get_dims_from_doc,
)

pytestmark = [pytest.mark.prometheus, pytest.mark.monitor_with_endpoints]


@pytest.mark.k8s
@pytest.mark.kubernetes
def test_prometheus_in_k8s(agent_image, minikube, k8s_observer, k8s_test_timeout):
    monitors = [
        {"type": "prometheus-exporter",
         "discoveryRule": 'container_image =~ "prometheus" && private_port == 9090',
         "useHTTPS": False,
         "skipVerify": True,
         "metricPath": "/metrics"},
    ]
    yamls = [os.path.join(os.path.dirname(os.path.realpath(__file__)), y) for y in ["prometheus.yaml"]]
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "metrics.txt"), "r") as fd:
        expected_metrics = {m.strip() for m in fd.readlines() if len(m.strip()) > 0}
    run_k8s_monitors_test(
        agent_image,
        minikube,
        monitors,
        yamls=yamls,
        observer=k8s_observer,
        expected_metrics=expected_metrics,
        test_timeout=k8s_test_timeout)
