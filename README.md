# rocks-quarry

## Overview

rocks-quarry is a python package lightly wrapping rocksdb with an http API. The http API allows
you to place objects of different forms into the database, then retrieve them or delete them
later.

## Installation

Install `python-rocksdb` according to the installation instructions for your system.
See [python-docksbd](https://python-rocksdb.readthedocs.io).

Then, simply clone the package and use it directly. I may eventually package it up into a proper
module.

## Usage

`python3 -m rocks_quarry --port=<port> --data-dir=<location_on_filesystem>`

### Example

To listen on port 8080 and store the database in /tmp/data, run:

`python3 -m rocks_quarry --port=8080 --data-dir="/tmp/data`

## API

The API is fairly straightforward. It supports three operations:

1. GET
2. PUT
3. DELETE

A major semantic of the API is that it distinguishes between paths ending with "/" and paths *not* ending with
a "/". Paths not ending with "/" are simple objects. Paths ending with "/" are collections, which slightly modifies the behaviour of operations on them. This will probably be simplified in the future.

All accesses are at path `/api/$API_VERSION/$object_path`. For example, if you want to access object "foo" in
the current version, you would access: `/api/v1alpha/foo`.

Paths are case sensitive.

Currently data is stored as unicode strings. In the future I want to use headers to indicate the data format to
allow binary data transer and storage.

### Version

The current API version is v1alpha.

### GET

Get allows you to retrieve previously stored objects. Gets of objects return the previously stored value in the body. A status of 200 means that the lookup succeeded. A status of 404 means that it failed because the object could not be found.

The following examples use curl for demonstration purposes.

#### Retrieving A Single Object

```text
$ curl localhost:8080/api/v1alpha/agilicus/awesome
true
```

Here we retrieved a previously stored object called "awesome" under the "agilicus" path. What would have happened
if we tried to retrieve something that did not exist?

```test
$curl localhost:8080/api/v1alpha/agilicus/sad
{"error": "key not found"}
```

#### Retrieving a Collection

Collections are retrieved by specifying the location of the collection terminated by a "/". The results
are returned as a json object rooted at the collection.

```text
$ curl localhost:8080/api/v1alpha/agilicus/
{"agilicus": {"awesome": "true", "hello": "world"}}
```

### PUT

Put allows you to create or replace a single object. Currently creation or modification of collections directly is not supported. The body of the request forms the data stored in the database.

#### Creating a Collection

This example creates the collection we retrieved earlier.

```text
curl -X PUT  lcalhost:8080/api/v1alpha/agilicus/ -d ''
curl -X PUT  localhost:8080/api/v1alpha/agilicus/hello -d 'world'
curl -X PUT  localhost:8080/api/v1alpha/agilicus/awesome -d 'true'
```

### DELETE

Delete lets you delete a single object or a collection. In both cases the return values are the same.

On success, a json object containing the number of items deleted and a list of deleted keys is returend.
On failure, an error is returned. A status of 200 indicates success. A status of 404 indicates that the
provided path could not be found.

#### Deleting a Single Obejct

This example creates and deletes an object. It then shows how it has been deleted by failing to access
it.

```text
$ curl -X PUT  localhost:8080/api/v1alpha/agilicus/foo -d 'bar'
$ curl -X DELETE  localhost:8080/api/v1alpha/agilicus/foo
{"total": 1, "deleted" : ["agilicus/foo"]}
$ curl localhost:8080/api/v1alpha/agilicus/foo
{"error": "key not found"}`
```

#### Deleting a Collection

This example deletes the "agilicus/" collection we created earlier.

```text
$ curl -X DELETE localhost:8080/api/v1alpha/agilicus/
{"total": 3, "deleted" : ["agilicus/", "agilicus/awesome", "agilicus/hello"]}
```

## Docker Container

We provide a docker container to aid with running the tool. To build it, simply run the following:

`docker build -t <your_tag> . -f docker/Dockerfile`

The container uses two environment variables to control execution. PORT and DATA_DIR. To run a container
listening on port 80, you can do the following:

```text
$docker run -ti -p 80:8080 -e PORT=8080 -e DBDIR=/tmp/test --rm --name test-server rocks-quarry
```

## License

rocks-quarry is licensed under the Apache2 license. See the LICENSE file under
the root directory for details.
