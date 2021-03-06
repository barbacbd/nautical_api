# NAUTICAL API 

[![Build](https://github.com/barbacbd/nautical_api/workflows/Build/badge.svg?branch=main&event=push)](https://github.com/barbacbd/nautical_api/actions/workflows/python-app.yml)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/barbacbd/nautical_api/pulse/commit-activity)
[![GitHub latest commit](https://img.shields.io/github/last-commit/barbacbd/nautical_api)](https://github.com/barbacbd/nautical_api/commit/)

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)


The project contains the API that can be used to expose the [nautical library](https://github.com/barbacbd/nautical). The goal
of this project is to provide a convenient method for users to interact with the nautical functions. Documentation for this project can
be found [here](https://barbacbd.github.io/nautical_api/).


# REST

The REST API utilizes `flask` to create a restful web service. When the package is installed, the
rest api application is installed as `nautical_rest`. The user can change the log level, port, and host.

## Endpoints

The api provides four endpoints.

### Sources

The `sources` endpoint will provide a list of objects. Each object contains the name of the source as
well as the endpoint to gather information about the source.

```bash
curl localhost:5000/sources
```

would return similar results to:

```json
{
    "sources": [
        {
            "id": "International Partners",
            "endpoint": "International_Partners"
        },
    ]
}
```

### Specific Sources

Each source that can be obtained from the output above, will also be an individual endpoint. This group of
endpoints are grouped together and internally termed the specific source endpoints.

```bash
curl localhost:5000/sources/<source_id>
```

Where the `<source_id>` is the field `endpoint` from the output of `/sources`. The result is a list of buoys
ids that are grouped together by the source.

```json
{
    "<source_id>": [
        <buoy_id1>, ...
    ]
}
```


### Buoys

The `buoys` endpoint will provide a list of all buoy ids.


```bash
curl localhost:5000/buoys
```

would return similar results to:

```json
{
    "buoys": [
        "<buoy_id1>",
	...
    ]
}
```

### Specific Buoys

Each buoy that can be obtained from the output above, will also be an individual endpoint. This group of
endpoints are grouped together and internally termed the specific buoy endpoints.

```bash
curl localhost:5000/buoys/<buoy_id>
```

Would return something similar to:

```json
{
    "<buoy_id>": {
       ... buoy data ...
    }
}
```
