import heapq
import collections
from typing import List

class Solution:
    def minimumTime(self, n: int, edges: List[List[int]], disappear: List[int]) -> List[int]:
        # 1. Construir o grafo (lista de adjacência)
        # Usamos um defaultdict para facilitar a adição de arestas
        graph = collections.defaultdict(list)
        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))

        # 2. Inicializar as estruturas de dados para Dijkstra
        # 'min_time' armazena o tempo mínimo conhecido para chegar a cada nó
        min_time = [float('inf')] * n
        # O tempo para chegar ao nó inicial (0) é 0
        min_time[0] = 0

        # Fila de prioridade (min-heap) para armazenar (tempo, nó)
        # Começamos com o nó 0 no tempo 0
        pq = [(0, 0)]

        # 'answer' guardará o resultado final
        answer = [-1] * n

        # 3. Executar o Algoritmo de Dijkstra modificado
        while pq:
            # Pega o nó com o menor tempo da fila
            time, u = heapq.heappop(pq)

            # Se já encontramos um caminho mais curto para 'u', ignoramos este
            if time > min_time[u]:
                continue
            
            # Se chegamos aqui, encontramos o caminho mais curto definitivo para 'u'
            answer[u] = time

            # 4. Explorar os vizinhos do nó 'u'
            for v, weight in graph[u]:
                new_time = time + weight

                # CONDIÇÃO PRINCIPAL:
                # O novo caminho só é válido se:
                # a) Chegamos no vizinho 'v' ANTES que ele desapareça.
                # b) Este novo caminho para 'v' é mais curto que o anterior.
                if new_time < disappear[v] and new_time < min_time[v]:
                    # Atualiza o tempo mínimo para 'v' e o adiciona na fila
                    min_time[v] = new_time
                    heapq.heappush(pq, (new_time, v))
        
        return answer