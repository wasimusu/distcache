from distcache.cache_client import CacheClient

client = CacheClient()

# Cache operations
client.set("brazil", "football")
client.set("harry", "potter")
client.set(1, 2)
client.set(3, 6)
client.set("hey", "hola")
client.get("hey")
client.get(1)
client.set("hey", "there")
client.get("hey")
client.delete(3)
client.get(3)
client.get("brazil")
