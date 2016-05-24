# py-lod4all

## What?

A Python library to access [LOD4ALL](http://lod4all.net/) and query a SPARQL

## Installation

As usual.

```shell
$ python setup.py install
```

## Example

```python
import lod4all

connection = lod4all.Connection(
    proxy_host=None,
    proxy_port=None,
    proxy_user=None,
    proxy_pass=None
)
query = 'SELECT DISTINCT * WHERE { <http://dbpedia.org/resource/Tokyo> ?p ?o . }'
response = connection.execute_sparql(query)

if response.success:
    for binding in response.data['results']['bindings']:
        # Do whatever with binding['o'] or binding['p']
else:
    # Error connecting to lod4all
    print(response.error_code)
```

