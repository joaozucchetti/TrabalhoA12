import networkx as nx
import matplotlib.pyplot as plt
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

source = 'V0'
source_idx = vertex_index[source]

INF = float('inf')
distance = {v: INF for v in vertices}
predecessor = {v: None for v in vertices}
distance[source] = 0

for _ in range(n - 1):
    for u, v, w in edges:
        if distance[u] != INF and distance[u] + w < distance[v]:
            distance[v] = distance[u] + w
            predecessor[v] = u

negative_cycle = False
for u, v, w in edges:
    if distance[u] != INF and distance[u] + w < distance[v]:
        negative_cycle = True
        break

print("=" * 80)
print("ALGORITMO DE BELLMAN-FORD - CAMINHOS MAIS CURTOS DESDE V0")
print("=" * 80)

print("\n1. ARRANJO DE DISTÂNCIAS (de V0):")
print("-" * 80)
dist_data = {}
for v in vertices:
    if distance[v] == INF:
        dist_data[v] = '∞'
    else:
        dist_data[v] = f'{distance[v]:.1f}'

dist_series = pd.Series(dist_data)
print(dist_series)

print("\n2. ARRANJO DE PREDECESSORES (de V0):")
print("-" * 80)
print(pd.Series(predecessor))

print("\n3. CAMINHOS MAIS CURTOS DE V0:")
print("-" * 80)
for v in vertices:
    if v != source:
        if distance[v] == INF:
            print(f"  {v}: ∞ (sem caminho)")
        else:
            # Reconstruct path
            path = []
            current = v
            while current is not None:
                path.append(current)
                current = predecessor[current]
            path.reverse()
            print(f"  {v}: distância = {distance[v]:.1f}, caminho = {' → '.join(path)}")

if negative_cycle:
    print("\n⚠️  AVISO: Ciclo de peso negativo detectado!")
else:
    print("\n✓ Nenhum ciclo de peso negativo detectado")

print("\n" + "=" * 80)

# Create SPT (Shortest Path Tree) visualization
print("\n4. ÁRVORE DE CUSTO MÍNIMO (desde V0):")
print("-" * 80)

# Build the shortest path tree
SPT = nx.DiGraph()
SPT.add_nodes_from(vertices)

for v in vertices:
    if v != source and predecessor[v] is not None:
        SPT.add_edge(predecessor[v], v, weight=distance[v] - distance[predecessor[v]])

print(f"Arestas da Árvore de Custo Mínimo:")
total_weight = 0
for u, v, data in SPT.edges(data=True):
    # Find the weight in the original graph
    for s, t, w in edges:
        if s == u and t == v:
            print(f"  {u} → {v}: {w}")
            total_weight += w
            break

print(f"\nCusto Total: {total_weight:.1f}")

# Visualization
print("\nGerando visualização da árvore de custo mínimo...")

pos = nx.spring_layout(G, seed=42, k=2, iterations=50)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Plot 1: Original graph with distances from source
ax1.set_title(f"Grafo Original\n(Distâncias de {source})", fontsize=14, fontweight='bold')
nx.draw_networkx_edges(G, pos, ax=ax1, alpha=0.5, edge_color='darkgray', style='dashed', width=2.5)
nx.draw_networkx_nodes(G, pos, ax=ax1, node_size=900, node_color='lightblue', edgecolors='darkblue', linewidths=3)

# Add distance labels inside nodes
labels_with_dist = {}
for v in vertices:
    if distance[v] == INF:
        labels_with_dist[v] = f"{v}\n(∞)"
    else:
        labels_with_dist[v] = f"{v}\n({distance[v]:.1f})"

nx.draw_networkx_labels(G, pos, ax=ax1, labels=labels_with_dist, font_size=11, font_weight='bold')

# Draw edges with weights
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, ax=ax1, edge_labels=edge_labels, font_size=10, font_weight='bold')

ax1.axis('off')

# Plot 2: Shortest Path Tree
ax2.set_title(f"Árvore de Custo Mínimo\n(Bellman-Ford de {source})", fontsize=14, fontweight='bold')
nx.draw_networkx_edges(G, pos, ax=ax2, alpha=0.1, edge_color='lightgray', style='dashed', width=1)
nx.draw_networkx_nodes(G, pos, ax=ax2, node_size=900, node_color='lightgreen', edgecolors='darkgreen', linewidths=3)
nx.draw_networkx_labels(G, pos, ax=ax2, labels=labels_with_dist, font_size=11, font_weight='bold')

# Draw SPT edges in red
if SPT.number_of_edges() > 0:
    nx.draw_networkx_edges(SPT, pos, ax=ax2, width=4, edge_color='darkred', alpha=0.9, 
                          arrowsize=25, arrowstyle='->', connectionstyle='arc3,rad=0.1')
    
    # Draw SPT edge labels
    spt_edge_labels = {}
    for u, v in SPT.edges():
        for s, t, w in edges:
            if s == u and t == v:
                spt_edge_labels[(u, v)] = f'{w}'
                break
    nx.draw_networkx_edge_labels(SPT, pos, ax=ax2, edge_labels=spt_edge_labels, font_size=10, font_weight='bold')

ax2.axis('off')

plt.tight_layout()
plt.show()

print("=" * 80)
