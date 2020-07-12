"""
Consistent Hashing

Consistent hashing is scheme which does not depend on the number of servers.
Each server is assigned a position on a abstract circle or a hash ring.

So you have a list of servers [a, b, c]\n
You make k copies of them. It makes the consistent hashing better.\n
servers = [a1, a2, ak, b1, b2, bk, c1, c2, ck]\n
Of course, you can have weighted servers so that better servers have higher chances of landing a keys.\n

Now we assign them a position in the 32bit ring.\n
[...ak....b2....c1....c2....a2.....b1....bk....a1.....ck..........]\n
[...10....19k...1M...28M....54.2M..60M...67M...100M...124M..23^32-1]\n
So we need to sort the servers according to their position.

Now when user says which server to send a particular key "apple".\n
We hash the key: apple-> 16M.\n
What's larger than 16M and has a server? 28M.\n
Great, we send the key to c2. c2 is c, remember?

What happens when a server is down?\n
There is no response and the query has to be queried against a database.\n
or any other function. And, it has to be stored again in the server.

If the server c went down. Our key ring would be updated to something like this.\n
[...ak....b2...........a2.....b1....bk....a1.................]\n
[...10....19k..........54.2M..60M...67M...100M........23^32-1]\n
We hash the key: apple-> 16M.\n
What's larger than 16M and has a server? 54.2M.\n
Great, we send the key to a2.

Similarly, we can add servers in the same way.\n
There will be cache misses first because the server next to the new server on the ring has the key.\n
Then those keys will expire out or will be LRU invalidated.\n
Similarly, there is cache miss when a server goes down. All the queries that were to be handed by that.\n
server are sent to the next server.

Notes: We compute position for servers until there is no collision.

Example usage:
    servers = ['192.168.0.246:11212', '192.168.0.247:11212', '192.168.0.249:11212']
    weights = [3, 3, 3]
    ring = ConsistentHashing(servers, weights)
    server = ring.get_node('my_key')

TODO: Allow users to specify both number of replicas and weight of servers
TODO: Use a better hashing technique. Something that distributes more uniformly among the keys.
"""
from bisect import bisect_right, insort


class ConsistentHashing:
    """
    Implements consistent hashing
    """

    def __init__(self, nodes=None, weights=None):
        """
        Initially we will make as may replicas as weight

        :param nodes: list of servers
        :param weights: the servers with higher usable capacity should have weights.
        """
        self.ring = []  # (position, server) in sorted order
        self.occupied = set()
        self.weight = 5
        if nodes and not weights:
            weights = [self.weight] * len(nodes)
        # The user can keep adding servers as the user discovers servers
        if nodes and len(nodes):
            self._generate_ring(nodes, weights)

    def _generate_ring(self, nodes, weights):
        for id, node in enumerate(nodes):
            for i in range(weights[id]):
                key = "{}_{}".format(node, i)
                position = hash(key)
                # If the position already exists hash again.
                while position in self.occupied:
                    key = "{}_{}".format(key, i)
                    position = hash(key)
                self.occupied.add(position)
                insort(self.ring, (position, node))

    def add_node(self, node, weight=5):
        """
        Add node to the HashRing of consistent hashing scheme.

        :param node: new node to be added (ip address in this case)
        :param weight: weight of the new node to be added.
        :return: None
        """
        self._generate_ring([node], [weight])

    def remove_node(self, node):
        """
        Remove node from the ring because it is dead or unavailable.

        :param node: node to be removed from the consistent hashing scheme.
        It will no longer be considered while hashing.

        :return: None
        """
        temp = []
        for position, server in self.ring:
            if server != node:
                temp.append((position, server))
                self.occupied.remove(position)
        self.ring = temp.copy()
        del temp

    def get_node(self, key):
        """
        Get the node/server where the key is or should be.

        :param key: key whose node/server is to be computed.
        :return: node where the key should be stored or retrived from.
        """
        position = bisect_right(self.ring, (hash(key), None))
        if position == len(self.ring):
            position = 0
        return self.ring[position][1]


if __name__ == '__main__':
    servers = ['192.168.0.246:11212',
               '192.168.0.247:11212',
               '192.168.0.249:11212']
    weights = [5, 3, 1]
    ring = ConsistentHashing(servers, weights)
    server = ring.get_node('my_key')
    print(server)

    ring.remove_node(server)

    server = ring.get_node('my_key')
    print(server)
