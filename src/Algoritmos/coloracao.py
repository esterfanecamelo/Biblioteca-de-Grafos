def coloracao_propria(self):
    cor = {v: None for v in self.lista_adj}

    for v in self.lista_adj:
        cores_usadas = set()

        # verifica cores dos vizinhos
        for viz, _ in self.lista_adj[v]:
            if cor[viz] is not None:
                cores_usadas.add(cor[viz])

        # escolhe a menor cor possível
        cor_atual = 1
        while cor_atual in cores_usadas:
            cor_atual += 1

        cor[v] = cor_atual

    total_cores = max(cor.values())
    return cor, total_cores
