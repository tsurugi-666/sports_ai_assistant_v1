class SemanticNetwork:
    def __init__(self):
        self.nodes = set()
        self.edges = [] # [(node1, relation, node2)]

    def add_node(self, node: str):
        self.nodes.add(node)

    def add_edge(self, source: str, relation: str, target: str):
        self.nodes.add(source)
        self.nodes.add(target)
        self.edges.append((source, relation, target))

    def get_related_objects(self, source: str, relation: str = None) -> list:
        results = []
        for src, rel, tgt in self.edges:
            if src.lower() == source.lower():
                if relation is None or rel == relation:
                    results.append((rel, tgt))
        return results