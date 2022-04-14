# NAUTICAL API

The project contains the APIs that can be used to expose the [nautical library](https://github.com/barbacbd/nautical). The goal
of this project is to provide a convenient method for users to interact with the nautical functions.


# APIs

## REST

The REST API utilizes `flask` to create a restful web service. When the package is installed, the
rest api application is installed as `nautical_rest`. The user can change the log level, port, and host.

### Endpoints

The api provides four endpoints.

#### Sources

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

#### Specific Sources

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


#### Buoys

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

#### Specific Buoys

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