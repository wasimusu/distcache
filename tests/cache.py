from distcache.cache_server import CacheServer
import time
import random
from PIL import Image

server = CacheServer(5)
server.spawn()

max_sleep = 5
server.set("wasim", "akram")
time.sleep(random.randint(0, max_sleep))

server.set("ram", "prasad")
time.sleep(random.randint(0, max_sleep))

server.set(1, 2)
time.sleep(random.randint(0, max_sleep))

server.set(3, 6)
time.sleep(random.randint(0, max_sleep))

server.set("hey", "bhaga")
time.sleep(random.randint(0, max_sleep))

server.get("hey")
time.sleep(random.randint(0, max_sleep))

server.get(1)
time.sleep(random.randint(0, max_sleep))

server.set("hey", "man")
time.sleep(random.randint(0, max_sleep))

server.get("hey")
time.sleep(random.randint(0, max_sleep))

server.delete(3)
time.sleep(random.randint(0, max_sleep))

server.get(3)
time.sleep(random.randint(0, max_sleep))

server.get("wasim")
time.sleep(random.randint(0, max_sleep))

server.close()
