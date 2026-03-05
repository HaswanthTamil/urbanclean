class MapGraph:

    def __init__(self):
        self.nodes = set()
        self.adj = {}

    def add_location(self, loc_id: str):
        if loc_id not in self.nodes:
            self.nodes.add(loc_id)
            self.adj[loc_id] = []

    def connect(self, a: str, b: str):
        if a not in self.nodes or b not in self.nodes:
            raise ValueError("Location not in graph")

        self.adj[a].append(b)
        self.adj[b].append(a)  

    def neighbors(self, loc_id: str):
        return self.adj.get(loc_id, [])
