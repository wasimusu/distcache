### Distributed Cache

This is project description and list of TODOs.

- Implement LRU eviction policy for cache
- (Optional) Implement consistent hashing
- (Optional) Implement health checks
- Deal with unavailable servers like cache miss.
When they come back online again, they will be treated as new servers.
- (Optional) Write the keyvalue to an underlying database i.e. a persistant storage. 
This allows dcache to also act as a key, value store database.

- Adding a server has two steps:
    * Start the server.
    * Ask the cache server to spwan. Then it will listen for new connections.