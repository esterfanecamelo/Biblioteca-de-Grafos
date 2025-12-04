from Grafo import Grafo

class Digrafo (Grafo):
    def __init__(self, dic, ):
        super().__init__(dic)

        self.lista_adj = {}
        for u, v, peso in self.arestas:
            if u not in self.lista_adj:
                self.lista_adj[u] = []
            if v not in self.lista_adj:
                self.lista_adj[v] = []
            self.lista_adj[u].append((v, peso))
       
        self.num_vertices = len(self.lista_adj)

# Retornar o númeoro de arestas do digrafo
def numero_arestas (self):
    return sum(len(vizinhos) for vizinhos in self.lista_adj.vaules())

