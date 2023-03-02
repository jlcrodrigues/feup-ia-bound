
RING_NUMBER = 4
NODES_PER_RING = 5

BLACK = 1
WHITE = 2

class Node:
    """
    A node in the graph. The level corresponds to which ring it is on.
    The pos is the number of the node in the ring.
    It also holds current piece and a set of neighbors (edges).
    """
    def __init__(self, level: int, pos: int, edges=None):
        self.level = level
        self.piece = 0 # 1 for white, 2 for black, 0 for none
        self.pos = pos
        if edges is None:
            edges = set()
        self.edges = edges # Set of indexes

    def __str__(self):
        node = "Ring " + str(self.level) + ", pos " + str(self.pos) + " "
        return node  + "-".join([str(edge) for edge in self.edges])

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def is_empty(self):
        return self.piece == 0

    def place_piece(self, piece):
        if not self.is_empty(): raise Exception('Error: Placing a piece in an occupied node.')
        self.piece = piece

    def remove_piece(self):
        if self.is_empty(): raise Exception('Error: Removing a piece from an unoccupied node.')
        self.piece = 0

    def add_edge(self, edge):
        self.edges.add(edge)

class Board:
    """
    Board of the game. Depending on the size, it will generate the nodes and edges.
    If no size is given, it will default to the standard pentagon shape.
    """
    def __init__(self, ring_number=RING_NUMBER, nodes_per_ring=NODES_PER_RING):
        self.ring_number = ring_number
        self.nodes_per_ring = nodes_per_ring
        self.nodes = []
        self.pieces = {BLACK: [], WHITE: []} # redundant storage of pieces for faster access

        self.generate()
        self.init_pieces()

    def generate(self):
        """Generates the initial game board, depending on the size."""
        for ring in range(self.ring_number):
            for pos in range(self.nodes_per_ring):
                node = Node(ring, pos)

                # Add same ring edges
                if (ring == 0 or ring == self.ring_number - 1):
                    node.add_edge(self.to_index((ring, pos + 1)))
                    node.add_edge(self.to_index((ring, pos - 1)))

                # Add next ring edges
                if ring < self.ring_number - 1:
                    node.add_edge(self.to_index((ring + 1, pos)))
                    if ring % 2 != 0: # Odd rings connect twice
                        node.add_edge(self.to_index((ring + 1, pos - 1)))

                # Add previous ring edges
                if ring > 0:
                    node.add_edge(self.to_index((ring - 1, pos)))
                    if ring % 2 == 0:
                        node.add_edge(self.to_index((ring - 1, pos + 1)))

                self.nodes.append(node)

    def to_index(self, coords: tuple):
        """Transform a tuple of coordinates into an index in the nodes list."""
        return coords[0] * self.nodes_per_ring + coords[1] % self.nodes_per_ring

    def to_coords(self, index: int):
        """Transform an index in the nodes list into a tuple of coordinates."""
        return (index // self.nodes_per_ring, index % self.nodes_per_ring)
    
    def init_pieces(self):
        """
        Place pieces on their initial position.
        Pieces are store both on each node, as well as in self.pieces
        This is done to streamline access to this info.
        """
        for piece in range(0, self.nodes_per_ring - 1):
            self.nodes[piece].place_piece(WHITE)
            self.pieces[WHITE].append((0, piece))

        first_outer = (self.ring_number - 1) * self.nodes_per_ring
        for piece in range(first_outer, first_outer + self.nodes_per_ring):
            if piece == first_outer + 1: continue
            self.nodes[piece].place_piece(BLACK)
            self.pieces[BLACK].append((self.ring_number - 1, piece % self.nodes_per_ring))

    def valid_move(self, player: int, source: tuple, dest: tuple):
        """
        Determines if a move can be executed.

            Parameters:
                player (int): Current player- 1 or 2.
                source (tuple): Source coordinated in the form (level, pos).
                dest (tuple): Destination coordinated in the form (level, pos).

            Returns:
                (bool): True if the move is valid, false otherwise.
        """
        dest_idx = self.to_index(dest)
        source_idx = self.to_index(source)

        if dest_idx in self.nodes[source_idx].edges:
            return self.nodes[dest_idx].piece == 0 and self.nodes[source_idx].piece == player
        return False

    def move(self, player: int, source: tuple, dest: tuple):
        """Move a player's piece from source to destination."""
        if not self.valid_move(player, source, dest): raise Exception("Invalid Move")
        self.nodes[self.to_index(source)].remove_piece()
        self.nodes[self.to_index(dest)].place_piece(player)

    def is_bound(self, piece: tuple):
        """Find if a piece is bound."""
        edges = self.nodes[self.to_index(piece)].edges
        for edge in edges:
            if self.nodes[edge].piece == 0: return False
        return True
    
    def did_bound(self, piece: tuple):
        """Check if a placed piece bounded any of its neighbors."""
        edges = self.nodes[self.to_index(piece)].edges
        for edge in edges:
            if self.is_bound(self.to_coords(edge)): return True
        return False
        
       