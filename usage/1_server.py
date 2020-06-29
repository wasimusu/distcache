from distcache.cache_server import CacheServer

server = CacheServer(5)
server.spawn()

# Cache operations
server.set("brazil", "football")
server.set("harry", "potter")
server.set(1, 2)
server.set(3, 6)
server.set("hey", "hola")
server.get("hey")
server.get(1)
server.set("hey", "there")
server.get("hey")
server.delete(3)
server.get(3)
server.get("brazil")
