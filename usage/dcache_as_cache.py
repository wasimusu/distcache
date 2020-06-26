from src.server import CacheServer
import time
import random

server = CacheServer(5)
server.spawn()
# server.spawn()
# server.spawn()

server.set("wasim", "akram")
time.sleep(random.randint(0,10))

server.set("ram", "prasad")
time.sleep(random.randint(0,10))

server.set(1, 2)
time.sleep(random.randint(0,10))

server.set(3, 6)
time.sleep(random.randint(0,10))

server.set("hey", "bhaga")
time.sleep(random.randint(0,10))

server.get("hey")
time.sleep(random.randint(0,10))

server.get(1)
time.sleep(random.randint(0,10))

server.set("hey", "man")
time.sleep(random.randint(0,10))

server.get("hey")
time.sleep(random.randint(0,10))

server.delete(3)
time.sleep(random.randint(0,10))

server.get(3)
time.sleep(random.randint(0,10))

server.get("wasim")
time.sleep(random.randint(0,10))
