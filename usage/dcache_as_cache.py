from src.server import CacheServer

server = CacheServer(5)
server.spawn()
# server.spawn()
# server.spawn()

server.set("wasim", "akram")
server.set("ram", "prasad")
server.set(1, 2)
server.set(3, 6)
server.set("hey", "bhaga")
server.get("hey")
server.get(1)
server.set("hey", "man")
server.get("hey")
server.delete(3)
server.get(3)
server.get("wasim")
