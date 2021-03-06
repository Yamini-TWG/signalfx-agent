<!--- GENERATED BY gomplate from scripts/docs/monitor-page.md.tmpl --->

# collectd/nginx

 Monitors an nginx instance using our fork of the
collectd nginx plugin based on the [collectd nginx
plugin](https://collectd.org/wiki/index.php/Plugin:nginx).

See the [integrations
doc](https://github.com/signalfx/integrations/tree/master/collectd-nginx)
for more information.


Monitor Type: `collectd/nginx`

[Monitor Source Code](https://github.com/signalfx/signalfx-agent/tree/master/internal/monitors/collectd/nginx)

**Accepts Endpoints**: **Yes**

**Multiple Instances Allowed**: Yes

## Configuration

| Config option | Required | Type | Description |
| --- | --- | --- | --- |
| `host` | **yes** | `string` |  |
| `port` | **yes** | `integer` |  |
| `name` | no | `string` |  |
| `url` | no | `string` | The full URL of the status endpoint; can be a template (**default:** `http://{{.Host}}:{{.Port}}/nginx_status`) |
| `username` | no | `string` |  |
| `password` | no | `string` |  |
| `timeout` | no | `integer` |  (**default:** `0`) |




## Metrics

This monitor emits the following metrics.  Note that configuration options may
cause only a subset of metrics to be emitted.

| Name | Type | Description |
| ---  | ---  | ---         |
| `connections.accepted` | cumulative | Connections accepted by Nginx Web Server |
| `connections.handled` | cumulative | Connections handled by Nginx Web Server |
| `nginx_connections.active` | gauge | Connections active in Nginx Web Server |
| `nginx_connections.reading` | gauge | Connections being read by Nginx Web Server |
| `nginx_connections.waiting` | gauge | Connections waited on by Nginx Web Server |
| `nginx_connections.writing` | gauge | Connections being written by Nginx Web Server |
| `nginx_requests` | cumulative | Requests handled by Nginx Web Server |



