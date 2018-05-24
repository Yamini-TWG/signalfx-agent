import os
import pytest

from tests.kubernetes.utils import (
    run_k8s_monitors_test,
    get_metrics_from_doc,
    get_dims_from_doc,
)

pytestmark = [pytest.mark.collectd, pytest.mark.spark, pytest.mark.monitor_with_endpoints]


@pytest.mark.k8s
@pytest.mark.kubernetes
def test_spark_in_k8s(agent_image, minikube, k8s_observer, k8s_test_timeout):
    monitors = [
        {"type": "collectd/spark",
         "discoveryRule": 'container_image =~ "spark" && private_port == 8080',
         "clusterType": "Standalone",
         "isMaster": True,
         "collectApplicationMetrics": True,
         "enhancedMetrics": True},
    ]
    yamls = [os.path.join(os.path.dirname(os.path.realpath(__file__)), y) for y in ["spark.yaml"]]
    run_k8s_monitors_test(
        agent_image,
        minikube,
        monitors,
        yamls=yamls,
        observer=k8s_observer,
        expected_metrics=get_metrics_from_doc("collectd-spark.md"),
        expected_dims=get_dims_from_doc("collectd-spark.md"),
        test_timeout=k8s_test_timeout)

