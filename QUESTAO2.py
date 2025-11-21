import networkx as nx
import matplotlib.pyplot as plt

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

G = nx.Graph()
G.add_weighted_edges_from(edges)

mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

total_cost = mst.size(weight='weight')

print("=" * 60)
print("ALGORITMO DE KRUSKAL - ÁRVORE GERADORA DE CUSTO MÍNIMO")
print("=" * 60)
print("\nArestas da Árvore Geradora Mínima:")
print("-" * 60)
for u, v, d in sorted(mst.edges(data=True)):
    print(f"  {u} - {v}: {d['weight']}")

print("-" * 60)
print(f"Custo Total da MST: {total_cost:.1f}")
print("=" * 60)

pos = nx.spring_layout(G, seed=42, k=2, iterations=50)

plt.figure(figsize=(12, 9))

nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='lightgray', style='dashed', width=1)
nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightgreen', edgecolors='black', linewidths=2)
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

nx.draw_networkx_edges(mst, pos, width=3, edge_color='blue', alpha=0.8)

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

plt.title(f"Árvore Geradora Mínima (Kruskal)\nCusto Total: {total_cost:.1f}", fontsize=16, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.show()
