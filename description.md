### Distributed Cache

This is project description and list of TODOs.

- Determine the size of the cache being used.
- Implement LRU eviction policy for cache
- Adding a server has two steps:
    * Start the server.
    * Ask the cache server to spwan. Then it will listen for new connections.

- ##### TODO for cache
- Handle timeout
- Implement increment and decrement in redis like counter
- Make sure it works for single server node
- Add benchmarks for databases
- Add sample code
- (Optional) Implement consistent hashing
- (Optional) Implement health checks
- Deal with unavailable servers like cache miss.
When they come back online again, they will be treated as new servers.

- ##### TODO for persistent storage
- Write in batches to the disk 
- When key is not in the cache, check for it in the disk

