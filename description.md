### Distributed Cache

This is project description and list of TODOs.

- Determine the size of the cache being used.
- Implement LRU eviction policy for cache
- Adding a server has two steps:
    * Start the server.
    * Ask the cache server to spwan. Then it will listen for new connections.
- Implement get, set, delete
- Handle timeout
- Log important stats like hits and misses
- Implement consistent hashing
- Deal with unavailable servers like cache miss.
When they come back online again, they will be treated as new servers.

- ##### TODO for cache
- Log reconstruction (persistent)
- Implement health checks
- Expiration time on keys. It just makes each record expensive to store.
- Implement increment and decrement in redis like counter
- Make sure it works for single server node
- Make some calls aysnc after testing code on single thread
- Add benchmarks for databases
    - Create 100,000 files of products. Read and query these files.
    - Create 100,000 files of random images maybe (binary). Read and query these files.
    - Note: For benchmarks, we consider reading from database/file directly versus having querying in-memory key, value store.     
- Add sample code

- ##### TODO for persistent storage
- Write in batches to the disk. Make provision for flush as well. 
- When key is not in the cache, check for it in the disk