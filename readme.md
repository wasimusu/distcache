### dcache (Distributed Cache)
dcache is a python open-source distributed in-memory cache and database.
Operations are mostly asynchronous to achieve high performance.
It is implemented purely in python without any external dependency.
One of design goal of this project is ease of use and less congitive load to users of
similar caching/database systems like Redis, Memcached.

#### Build and test status
<img src="https://travis-ci.com/wasimusu/dcache.svg?branch=master" width="100">

### Features
- The cache could be on a single PC or multiple PCs scattered over the internet.
- Hardware failure is accounted for
- Cache is available unless all PCs fail
- The API is similar to memcached

# Platform
* Linux
* Python 2.7 to Python 3.5

#### Storage Commands
- set (can be used to update as well, updates the LRU too)
- add
- delete

#### Retrieval Commands
- get
- gets

### TODO
- Add tests
- Add benchmarks

### Install
```
pip install -r requirements.txt
```

### Usage


### Contributing
Please read [contributing] (contributing.md) to learn how to contribute to this project.