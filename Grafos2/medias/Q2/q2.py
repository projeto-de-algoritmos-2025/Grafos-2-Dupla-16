import heapq


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # Construir o grafo como lista de adjacência
        graph = {i: [] for i in range(1, n + 1)}
        for u, v, w in times:
            graph[u].append((v, w))  # u -> (v, peso)

        # Distâncias começam como infinito
        dist = {i: float('inf') for i in range(1, n + 1)}
        dist[k] = 0  # distância da fonte para ela mesma é 0

        # Min-heap (custo acumulado, nó atual)
        heap = [(0, k)]

        while heap:
            time, node = heapq.heappop(heap)

            # Se já achamos um caminho melhor antes, ignoramos
            if time > dist[node]:
                continue

            # Explorar vizinhos
            for nei, w in graph[node]:
                new_time = time + w
                if new_time < dist[nei]:
                    dist[nei] = new_time
                    heapq.heappush(heap, (new_time, nei))

        # A resposta é o maior tempo mínimo encontrado
        ans = max(dist.values())
        return ans if ans != float('inf') else -1
