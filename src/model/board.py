
RING_NUMBER = 4
NODES_PER_RING = 5


class Node:
    """
    A node in the graph. The level corresponds to which ring it is on.
    The pos is the number of the node in the ring.
    It also holds current piece and a set of neighbors (edges).
    """
    def __init__(self, level, pos, edges=None):
        self.level = level
        self.piece = 0 # 1 for white, 2 for black, 0 for none
        self.pos = pos
        if edges is None:
            edges = set()
        self.edges = edges

    def __str__(self):
        node = "Ring " + str(self.level) + ", pos " + str(self.pos) + " "
        return node  + "-".join([str(edge) for edge in self.edges])

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def place_piece(self, piece):
        self.piece = piece

    def add_edge(self, edge):
        self.edges.add(edge)

    def print_edges(self):
        for edge in self.edges:
            print(edge)


class Board:
    """
    Board of the game. Depending on the size, it will generate the nodes and edges.
    If no size is given, it will default to the standard pentagon shape.
    """
    def __init__(self, ring_number=RING_NUMBER, nodes_per_ring=NODES_PER_RING):
        self.ring_number = ring_number
        self.nodes_per_ring = nodes_per_ring
        self.nodes = []

        self.generate()

    def generate(self):
        for ring in range(self.ring_number):
            for pos in range(self.nodes_per_ring):
                node = Node(ring, pos)

                # Add same ring edges
                if (ring == 0 or ring == self.ring_number - 1):
                    node.add_edge(ring * self.nodes_per_ring + (pos + 1) % self.nodes_per_ring)
                    node.add_edge(ring * self.nodes_per_ring + (pos - 1) % self.nodes_per_ring)

                # Add next ring edges
                if ring < self.ring_number - 1:
                    node.add_edge((ring + 1) * self.nodes_per_ring + pos)
                    if ring % 2 != 0: # Odd rings connect twice
                        node.add_edge((ring + 1) * self.nodes_per_ring + (pos - 1) % self.nodes_per_ring)

                # Add previous ring edges
                if ring > 0:
                    node.add_edge((ring - 1) * self.nodes_per_ring + pos)
                    if ring % 2 == 0:
                        node.add_edge((ring - 1) * self.nodes_per_ring + (pos + 1) % self.nodes_per_ring)

                self.nodes.append(node)
