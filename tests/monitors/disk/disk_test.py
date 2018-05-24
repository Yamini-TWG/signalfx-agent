import os
import pytest

from tests.kubernetes.utils import (
    run_k8s_monitors_test,
    get_metrics_from_doc,
    get_dims_from_doc,
)

pytestmark = [pytest.mark.collectd, pytest.mark.disk, pytest.mark.monitor_without_endpoints]


@pytest.mark.k8s
@pytest.mark.kubernetes
def test_disk_in_k8s(agent_image, minikube, k8s_test_timeout):
    monitors = [
        {"type": "collectd/disk"}
    ]
    run_k8s_monitors_test(
        agent_image,
        minikube,
        monitors,
        expected_metrics=get_metrics_from_doc("collectd-disk.md"),
        expected_dims=get_dims_from_doc("collectd-disk.md"),
        test_timeout=k8s_test_timeout)

