# NAUTICAL API 

[![Build](https://github.com/barbacbd/nautical_api/workflows/Build/badge.svg?branch=main&event=push)](https://github.com/barbacbd/nautical_api/actions/workflows/python-app.yml)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/barbacbd/nautical_api/pulse/commit-activity)
[![GitHub latest commit](https://img.shields.io/github/last-commit/barbacbd/nautical_api)](https://github.com/barbacbd/nautical_api/commit/)

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)


The project contains the API that can be used to expose the [nautical library](https://github.com/barbacbd/nautical). The goal
of this project is to provide a convenient method for users to interact with the nautical functions.


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


# Generating Documentation

Sphinx is used to generate the documentation for this project. Only documentation on the `main` branch will be published to the [github pages](https://barbacbd.github.io/nautical_api/html/index.html).

To generate documentation ensure that there is a `Makefile`, `make.bat`, `conf.py`, and `index.rst` file in the base project directory. The `conf.py` file should be updated each time that a project
version changes. The `index.rst` will _NOT_ change, but the rst files in rst_docs _should_ be (re)generated each time that new functionality or documentation change. Run the following command from
the project home directory.

```bash
sphinx-apidoc -f -o rst_docs nautical_api
```

If the documentation is already generated, then the generator must be careful not to remove the extra files in `./docs`. There is a `.nojekyll` file (empty) that exists, please be sure that this file
remains when performing a `make clean`. Similarly there is an extra `index.html` in the same directory. If these files are removed, revert or reset the change so that they persist.

From the project home run the command `make html` and the required html files will be generated in `docs`. Add the changes and commit them to provide the updated documentation.

```bash
# clean all of the docs
# leaving the index and nojekyll files
make clean

# regenerate the documents 
make html

git add docs/*
```
