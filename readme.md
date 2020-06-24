### dcache (Distributed Cache)

#### Build and test status
<img src="https://travis-ci.com/wasimusu/graphs.svg?branch=master" width="100">

Distributed cache implemented in pure python without any external dependency.

### Features
- The cache could be on a single PC or multiple PCs scattered over the internet.
- Hardware failure is accounted for
- Cache is available unless all PCs fail
- The API is similar to memcached

# Platform
* Windows
* Linux

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
- Add Travis CI

### System Requirements
Runs on both windows and linux platforms
Requires python3


### Install
```
pip install -r requirements.txt
```

### Usage


### Contributing
