import networkx as nx
import numpy as np
import pandas as pd

edges = [
    ('V0', 'V1', 1.0),
    ('V0', 'V2', 5.0),
    ('V0', 'V3', 5.3),
    ('V1', 'V4', 1.9),
    ('V2', 'V1', 0.3),
    ('V2', 'V3', 0.5),
    ('V2', 'V4', 0.3),
    ('V3', 'V5', 5.0),
    ('V4', 'V5', 1.3),
    ('V5', 'V2', 9.1)
]

G = nx.DiGraph()
G.add_weighted_edges_from(edges)

vertices = sorted(G.nodes())
n = len(vertices)
vertex_index = {v: i for i, v in enumerate(vertices)}
index_vertex = {i: v for i, v in enumerate(vertices)}

INF = float('inf')
dist = [[INF] * n for _ in range(n)]
pred = [[None] * n for _ in range(n)]

for i in range(n):
    dist[i][i] = 0

for u, v, w in edges:
    i, j = vertex_index[u], vertex_index[v]
    dist[i][j] = w
    pred[i][j] = u

for k in range(n):
    for i in range(n):
        for j in range(n):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
                pred[i][j] = pred[i][k]

# Print results
print("=" * 80)
print("ALGORITMO DE FLOYD-WARSHALL - CAMINHOS MAIS CURTOS")
print("=" * 80)

# Print Distance Matrix
print("\n1. MATRIZ DE DISTÂNCIAS:")
print("-" * 80)
dist_df = pd.DataFrame(dist, index=vertices, columns=vertices)
# Replace infinity with 'INF' for display
dist_display = dist_df.copy()
dist_display = dist_display.applymap(lambda x: '∞' if x == INF else f'{x:.1f}')
print(dist_display)

# Print Predecessor Matrix
print("\n2. MATRIZ DE PREDECESSORES:")
print("-" * 80)
pred_df = pd.DataFrame(pred, index=vertices, columns=vertices)
print(pred_df)

# Print shortest paths from each vertex
print("\n3. CAMINHOS MAIS CURTOS:")
print("-" * 80)
for i in range(n):
    source = index_vertex[i]
    print(f"\nDe {source} para:")
    for j in range(n):
        if i != j:
            target = index_vertex[j]
            distance = dist[i][j]
            if distance == INF:
                print(f"  {target}: ∞ (sem caminho)")
            else:
                # Reconstruct path
                path = []
                current = j
                while current is not None and current != i:
                    path.append(index_vertex[current])
                    if pred[i][current] is not None:
                        current = vertex_index[pred[i][current]]
                    else:
                        break
                path.append(source)
                path.reverse()
                print(f"  {target}: distância = {distance:.1f}, caminho = {' → '.join(path)}")

print("\n" + "=" * 80)
