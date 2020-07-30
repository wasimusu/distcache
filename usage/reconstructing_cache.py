from distcache.cache_server import CacheServer

server = CacheServer(5)
server.replay_log()