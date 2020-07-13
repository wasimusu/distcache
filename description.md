### Distributed Cache

This is project description and list of TODOs.

##### Completed tasks
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
- Implement health checks
- (De)Serialization of key cache operations so that it can be reconstructed in the event of crash
- Decouple cache design from cache client. Allows you to swap the cache design on the fly.
And opens up cache design for testing.
- Restructure the project so that files can be imported properly.
- Add setup.py and other information for pypi.
- Write documentation
- Write in batches to the disk. Make provision for flush as well. 
- Implement increment and decrement in redis like counter

##### TODO for Release/General
- Make some calls aysnc after testing code on single thread
- Test everything!
    - Test all the different types of objects supported
    - Test cache
    - Test consistent hashing. Make it more uniform
    - Test heartbeat/health check
    - Test logger
    - Test communication (maybe the hardest part)
    - Test serialization (and probably replace it with a faster library)
- Add benchmarks for databases
    - Create 100,000 files of products. Read and query these files.
    - Create 100,000 files of random images maybe (binary). Read and query these files.
    - Note: For benchmarks, we consider reading from database/file directly versus having querying in-memory key, value store.     
- Add lots of sample code
- Write wiki

##### TODO for communication
- CacheServer starts HealthServers. CacheClients start HealthClients. 
- Make sure it works for single server node i.e. 
the communication between client and server works flawlessly. Cache is fine. :)
- Allow users to change the communication protocol: TCP/UDP/Unix Sockets.

##### TODO for persistent storage
- Write binary objects (image, pdfs, etc) to the disk
- When key is not in the cache, check for it in the disk/database

##### TODO for Cache Design
- Expiration time on keys. It just makes each record expensive to store.
- Implement different types of cache eviction strategies like LFU, etc.
- Determine the size of the cache being used.
