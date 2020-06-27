from distcache.cache_server import CacheServer

server = CacheServer(5)
server.spawn()
# server.spawn()
# server.spawn()

server.reconstruct_from_log()

server.close()
