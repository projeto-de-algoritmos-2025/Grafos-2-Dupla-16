
class Solution:
    def criticalConnections(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        # Grafo como lista de adjacência
        graph = defaultdict(list)
        for u, v in connections:
            graph[u].append(v)
            graph[v].append(u)
        
        # Arrays auxiliares
        self.time = 0
        disc = [-1] * n   # discovery time
        low = [-1] * n    # menor discovery time alcançável
        res = []

        def dfs(u, parent):
            disc[u] = low[u] = self.time
            self.time += 1

            for v in graph[u]:
                if v == parent:
                    continue
                if disc[v] == -1:
                    dfs(v, u)
                    low[u] = min(low[u], low[v])

                    # Se a aresta (u, v) é uma ponte
                    if low[v] > disc[u]:
                        res.append([u, v])
                else:
                    # Atualiza low-link em caso de back edge
                    low[u] = min(low[u], disc[v])

        # O grafo pode ser conexo, mas rodamos DFS de todos
        for i in range(n):
            if disc[i] == -1:
                dfs(i, -1)

        return res
