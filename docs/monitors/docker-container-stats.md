<!--- GENERATED BY gomplate from scripts/docs/monitor-page.md.tmpl --->

# docker-container-stats

 This monitor reads container stats from a
Docker API server.  It is meant as a metric-compatible replacement of our
[docker-collectd](https://github.com/signalfx/docker-collectd-plugin)
plugin, which scales rather poorly against a large number of containers.

This currently does not support CPU share/quota metrics.

If you are running the agent directly on a host (outside of a container
itself) and you are using the default Docker UNIX socket URL, you will
probably need to add the `signalfx-agent` user to the `docker` group in
order to have permission to access the Docker API via the socket.

Requires Docker API version 1.22+.


Monitor Type: `docker-container-stats`

[Monitor Source Code](https://github.com/signalfx/signalfx-agent/tree/master/internal/monitors/docker)

**Accepts Endpoints**: No

**Multiple Instances Allowed**: Yes

## Configuration

| Config option | Required | Type | Description |
| --- | --- | --- | --- |
| `dockerURL` | no | `string` | The URL of the docker server (**default:** `unix:///var/run/docker.sock`) |
| `timeoutSeconds` | no | `integer` | The maximum amount of time to wait for docker API requests (**default:** `5`) |
| `labelsToDimensions` | no | `map of string` | A mapping of container label names to dimension names. The corresponding label values will become the dimension value for the mapped name.  E.g. `io.kubernetes.container.name: container_spec_name` would result in a dimension called `container_spec_name` that has the value of the `io.kubernetes.container.name` container label. |
| `excludedImages` | no | `list of string` | A list of filters of images to exclude.  Supports literals, globs, and regex. |




## Metrics

This monitor emits the following metrics.  Note that configuration options may
cause only a subset of metrics to be emitted.

| Name | Type | Description |
| ---  | ---  | ---         |
| `blkio.io_service_bytes_recursive.async` | cumulative | Volume, in bytes, of asynchronous block I/O |
| `blkio.io_service_bytes_recursive.read` | cumulative | Volume, in bytes, of reads from block devices |
| `blkio.io_service_bytes_recursive.sync` | cumulative | Volume, in bytes, of synchronous block I/O |
| `blkio.io_service_bytes_recursive.total` | cumulative | Total volume, in bytes, of all block I/O |
| `blkio.io_service_bytes_recursive.write` | cumulative | Volume, in bytes, of writes to block devices |
| `blkio.io_serviced_recursive.async` | cumulative | Number of asynchronous block I/O requests |
| `blkio.io_serviced_recursive.read` | cumulative | Number of reads requests from block devices |
| `blkio.io_serviced_recursive.sync` | cumulative | Number of synchronous block I/O requests |
| `blkio.io_serviced_recursive.total` | cumulative | Total number of block I/O requests |
| `blkio.io_serviced_recursive.write` | cumulative | Number of write requests to block devices |
| `cpu.percent` | gauge | Percentage of host CPU resources used by the container |
| `cpu.percpu.usage` | cumulative | Jiffies of CPU time spent by the container, per CPU core |
| `cpu.percpu.usage` | cumulative | Jiffies of CPU time spent by the container, per CPU core |
| `cpu.throttling_data.periods` | cumulative | Number of periods |
| `cpu.throttling_data.throttled_periods` | cumulative | Number of periods throttled |
| `cpu.throttling_data.throttled_time` | cumulative | Throttling time in nano seconds |
| `cpu.usage.kernelmode` | cumulative | Jiffies of CPU time spent in kernel mode by the container |
| `cpu.usage.system` | cumulative | Jiffies of CPU time used by the system |
| `cpu.usage.total` | cumulative | Jiffies of CPU time used by the container |
| `cpu.usage.usermode` | cumulative | Jiffies of CPU time spent in user mode by the container |
| `memory.stats.swap` | gauge | Bytes of swap memory used by container |
| `memory.usage.limit` | gauge | Memory usage limit of the container, in bytes |
| `memory.usage.max` | gauge | Maximum measured memory usage of the container, in bytes |
| `memory.usage.total` | gauge | Bytes of memory used by the container |
| `network.usage.rx_bytes` | cumulative | Bytes received by the container via its network interface |
| `network.usage.rx_dropped` | cumulative | Number of inbound network packets dropped by the container |
| `network.usage.rx_errors` | cumulative | Errors receiving network packets |
| `network.usage.rx_packets` | cumulative | Network packets received by the container via its network interface |
| `network.usage.tx_bytes` | cumulative | Bytes sent by the container via its network interface |
| `network.usage.tx_dropped` | cumulative | Number of outbound network packets dropped by the container |
| `network.usage.tx_errors` | cumulative | Errors sending network packets |
| `network.usage.tx_packets` | cumulative | Network packets sent by the container via its network interface |



