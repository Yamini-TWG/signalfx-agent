<!--- GENERATED BY gomplate from scripts/docs/monitor-page.md.tmpl --->

# collectd/custom

 This monitor lets you provide custom collectd
configuration to be run by the managed collectd instance.  The provided
config is parsed as a Go template, so if you provide a `discoveryRule` to
automatically discover service endpoints, the agent will create a separate
copy of the config for each endpoint discovered and fill in the `{{.Host}}`
and `{{.Port}}` parameters in the provided config with those of the
discovered endpoint.  If you do not provide a discovery rule, the provided
config will be run immediately with collectd.

You can provide configuration for as many plugins as you want in a single
instance of this monitor configuration.

You can also use your own Python plugins in conjunction with the
`ModulePath` option in
[collectd-python](https://collectd.org/documentation/manpages/collectd-python.5.shtml).
If your Python plugin has dependencies of its own, you can specify the path
to them by specifying multiple `ModulePath` options with those paths.

Here is an example of a configuration with a custom Python plugin:

```yaml
  - type: collectd/custom
    discoveryRule: containerImage =~ "myservice"
    template: |
      LoadPlugin "python"
      <Plugin python>
        ModulePath "/usr/lib/python2.7/dist-packages/health_checker"
        Import "health_checker"
        <Module health_checker>
          URL "http://{{.Host}}:{{.Port}}"
          JSONKey "isRunning"
          JSONVal "1"
        </Module>
      </Plugin>
```


Monitor Type: `collectd/custom`

[Monitor Source Code](https://github.com/signalfx/signalfx-agent/tree/master/internal/monitors/collectd/custom)

**Accepts Endpoints**: **Yes**

**Multiple Instances Allowed**: Yes

## Configuration

| Config option | Required | Type | Description |
| --- | --- | --- | --- |
| `host` | no | `string` | This should generally not be set manually, but will be filled in by the agent if using service discovery. It can be accessed in the provided config template with `{{.Host}}`.  It will be set to the hostname or IP address of the discovered service. If you aren't using service discovery, you can just hardcode the host/port in the config template and ignore these fields. |
| `port` | no | `integer` | This should generally not be set manually, but will be filled in by the agent if using service discovery. It can be accessed in the provided config template with `{{.Port}}`.  It will be set to the port of the discovered service, if it is a TCP/UDP endpoint. (**default:** `0`) |
| `name` | no | `string` | This should generally not be set manually, but will be filled in by the agent if using service discovery. It can be accessed in the provided config template with `{{.Name}}`.  It will be set to the name that the observer creates for the endpoint upon discovery.  You can generally ignore this field. |
| `template` | no | `string` | A config template for collectd.  You can include as many plugin blocks as you want in this value.  It is rendered as a standard Go template, so be mindful of the strings `{{` and `}}`. |
| `templates` | no | `list of string` | A list of templates, but otherwise equivalent to the above `template` option.  This enables you to have a single directory with collectd configuration files and load them all by using a globbed remote config value: |





