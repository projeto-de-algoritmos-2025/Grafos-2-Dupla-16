from typing import List

class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # Anexa índice original e ordena por peso
        for i, e in enumerate(edges):
            e.append(i)  # agora e = [u, v, w, idx]
        edges.sort(key=lambda x: x[2])
        m = len(edges)

        # DSU com path compression + union by size
        class DSU:
            def __init__(self, n):
                self.parent = list(range(n))
                self.size = [1] * n
                self.components = n

            def find(self, x):
                while self.parent[x] != x:
                    self.parent[x] = self.parent[self.parent[x]]
                    x = self.parent[x]
                return x

            def union(self, a, b):
                ra, rb = self.find(a), self.find(b)
                if ra == rb:
                    return False
                # union by size
                if self.size[ra] < self.size[rb]:
                    ra, rb = rb, ra
                self.parent[rb] = ra
                self.size[ra] += self.size[rb]
                self.components -= 1
                return True

        # Kruskal generalizado: skip = índice em edges (posição ordenada) a pular
        # pick = índice em edges (posição ordenada) a forçar (incluir antes)
        def mst_weight(skip: int = -1, pick: int = -1) -> float:
            dsu = DSU(n)
            weight = 0
            used = 0

            # Se pedir incluir uma aresta, inclua primeiro
            if pick != -1:
                u, v, w, _ = edges[pick]
                if dsu.union(u, v):
                    weight += w
                    used += 1

            for i in range(m):
                if i == skip:
                    continue
                u, v, w, _ = edges[i]
                if dsu.union(u, v):
                    weight += w
                    used += 1
                    # se já conectou tudo, podemos parar
                    if used == n - 1:
                        break
                # pequeno corte: se já passou do peso base (quando conhecido) pode interromper
            return weight if dsu.components == 1 else float('inf')

        # MST base (sem skip/pick)
        base = mst_weight()

        critical = []
        pseudo = []

        for i in range(m):
            # Testar removendo a aresta i (pular)
            w_without = mst_weight(skip=i)
            if w_without > base:
                # se remover aumentou o custo ou desconectou -> crítica
                critical.append(edges[i][3])  # índice original
            else:
                # testar forçar inclusão da aresta i
                w_with = mst_weight(pick=i)
                if w_with == base:
                    pseudo.append(edges[i][3])

        return [critical, pseudo]
