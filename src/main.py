from Grafo import Grafo
from Digrafo import Digrafo
import os

def ler_arquivo(caminho_arquivo):
    dados = {
        "num_vertices": 0,
        "num_arestas": 0,
        "arestas": [],
        "adj": {}
    }

    with open(caminho_arquivo, "r") as f:
        for linha in f:
            linha = linha.strip()

            if not linha or linha.startswith("c"):
                continue

            # Linha do problema: p sp <num_vertices> <num_arestas>
            if linha.startswith("p"):
                partes = linha.split()
                # Exemplo: p sp 264346 733846
                if len(partes) >= 4:
                    dados["num_vertices"] = int(partes[2])
                    dados["num_arestas"] = int(partes[3])
                continue

            # Linha de arco: a x y p
            if linha.startswith("a"):
                _, u, v, peso = linha.split()
                u, v, peso = int(u), int(v), float(peso)

                dados["arestas"].append((u, v, peso))

                if u not in dados["adj"]:
                    dados["adj"][u] = []
                dados["adj"][u].append((v, peso))

    return dados


# Caminho da pasta dados
base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dados"))

arquivo_grafo = os.path.join(base, "grafos_teste.gr")
arquivo_digrafo = os.path.join(base, "USA-road-d.NY.gr")
#arquivo_digrafo = os.path.join(base, "digrafo_teste.gr")

# Carregar grafos
grafo_dict = ler_arquivo(arquivo_grafo)
digrafo_dict = ler_arquivo(arquivo_digrafo)

G = Grafo(grafo_dict)
D = Digrafo(digrafo_dict)


# ---------------- MENU ---------------- #

def menu_grafo():
    while True:
        print("\n===== MENU GRAFO =====")
        print("1 - Número de vértices")
        print("2 - Número de arestas")
        print("3 - Vizinhos de um vértice")
        print("4 - Grau do vértice")
        print("5 - Peso da aresta")
        print("6 - Grau mínimo e máximo")
        print("7 - BFS")
        print("8 - DFS")
        print("9 - Bellman-Ford")
        print("10 - Dijkstra")
        print("11 - Coloração própria")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            print("Vértices:", G.numero_de_vertices())

        elif op == "2":
            print("Arestas:", G.numero_de_arestas())

        elif op == "3":
            v = int(input("Vértice: "))
            print("Vizinhos:", G.retornar_vizinhos(v))

        elif op == "4":
            v = int(input("Vértice: "))
            print("Grau:", G.grau_do_vertice(v))

        elif op == "5":
            u = int(input("u: "))
            v = int(input("v: "))
            print("Peso:", G.peso_da_aresta(u, v))

        elif op == "6":
            print("Grau mínimo:", G.grau_min())
            print("Grau máximo:", G.grau_max())

        elif op == "7":
            v = int(input("Origem BFS: "))
            d, pi = G.bfs(v)
            print("Distâncias:", d)
            print("Pais:", pi)

        elif op == "8":
            v = int(input("Origem DFS: "))
            pi, ini, fim = G.dfs(v)
            print("PI:", pi)
            print("Tempo inicial:", ini)
            print("Tempo final:", fim)

        elif op == "9":
            v = int(input("Origem BF: "))
            d, pi = G.bellman_ford(v)
            print("Distâncias:", d)
            print("Pais:", pi)

        elif op == "10":
            v = int(input("Origem Dijkstra: "))
            d, pi = G.dijkstra(v)
            print("Distâncias:", d)
            print("Pais:", pi)

        elif op == "11":
            cores, k = G.coloracao_propria()
            print("Cores:", cores)
            print("Total de cores:", k)

        elif op == "0":
            break

        else:
            print("Opção inválida.")


def menu_digrafo():
    while True:
        print("\n===== MENU DÍGRAFO =====")
        print("1 - Número de vértices")
        print("2 - Número de arestas")
        print("3 - Vizinhança de um vértice")
        print("4 - Grau de entrada / saída")
        print("5 - Peso da aresta")
        print("6 - BFS")
        print("7 - DFS")
        print("8 - Bellman-Ford")
        print("9 - Dijkstra")
        print("10 - Caminho com mínimo de arestas")
        print("11 - Ciclo com mínimo de arestas")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            print("Vértices:", D.numero_de_vertices())

        elif op == "2":
            print("Arestas:", D.numero_de_arestas())

        elif op == "3":
            v = int(input("Vértice: "))
            print("Vizinhos:", D.retornar_vizinhos(v))

        elif op == "4":
            v = int(input("Vértice: "))
            print("Entrada:", D.grau_de_entrada(v))
            print("Saída:", D.grau_de_saida(v))

        elif op == "5":
            u = int(input("u: "))
            v = int(input("v: "))
            print("Peso:", D.peso_da_aresta(u, v))

        elif op == "6":
            v = int(input("Origem BFS: "))
            d, pi = D.bfs(v)
            print("Distâncias:", d)
            print("Pais:", pi)

        elif op == "7":
            v = int(input("Origem DFS: "))
            pi, ini, fim = D.dfs(v)
            print("PI:", pi)
            print("Tempo inicial:", ini)
            print("Tempo final:", fim)

        elif op == "8":
            v = int(input("Origem BF: "))
            d, pi = D.bellman_ford(v)
            print("Distâncias:", d)
            print("Pais:", pi)

        elif op == "9":
            v = int(input("Origem Dijkstra: "))
            d, pi = D.dijkstra(v)
            print("Distâncias:", d)
            print("Pais:", pi)
            
        elif op == "10":
            minimo = int(input("Quantidade mínima de arestas: "))
            origem = int(input("Vértice de origem (ou 0 para qualquer): "))

            if origem == 0:
                caminho = D.caminho_com_arestas_minimas(minimo)
            else:
                caminho = D.caminho_com_arestas_minimas(minimo, origem)

            if caminho:
                print("Caminho encontrado:", caminho)
                print("Quantidade de arestas:", len(caminho) - 1)
            else:
                print("Nenhum caminho com essa quantidade de arestas foi encontrado.")
                
        elif op == "11":
            minimo = int(input("Quantidade mínima de arestas do ciclo: "))
            ciclo = D.ciclo_com_arestas_minimas(minimo)

            if ciclo:
                print("Ciclo encontrado:", ciclo)
                print("Quantidade de arestas:", len(ciclo) - 1)
            else:
                print("Nenhum ciclo com essa quantidade mínima foi encontrado.")

        elif op == "0":
            break

        else:
            print("Opção inválida.")


# --------------- MENU PRINCIPAL --------------- #
def main():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Testar Grafo")
        print("2 - Testar Dígrafo")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            menu_grafo()

        elif op == "2":
            menu_digrafo()

        elif op == "0":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
