# Set plotting style
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def plot_binomial_tree(stock_tree, option_tree, N):

    G = nx.Graph()
    for i in range(N+1):
        for j in range(i+1):
            node_id = f"{i},{j}"
            stock_price = stock_tree[i, j]
            option_value = option_tree[i, j]

            G.add_node(node_id, pos=(i, j), stock_price=stock_price, option_value=option_value)
            
            if i < N:
                G.add_edge(node_id, f"{i+1},{j}")
                G.add_edge(node_id, f"{i+1},{j+1}")


    pos = {}
    for node in G.nodes():
        i, j = map(int, node.split(','))
        pos[node] = (i, j - i/2)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Set titles
    fig.suptitle(f"European Call Option - Binomial Tree (N={N})")
    ax1.set_title("Stock Price Tree")
    ax2.set_title("Option Value Tree")
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax1, alpha=0.3)
    nx.draw_networkx_edges(G, pos, ax=ax2, alpha=0.3)
    
    # Draw nodes
    node_colors1 = [stock_tree[int(node.split(',')[0]), int(node.split(',')[1])] for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax1, node_size=700, node_color='lightblue')
    
    node_colors2 = [option_tree[int(node.split(',')[0]), int(node.split(',')[1])] for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax2, node_size=700, node_color='lightcoral')
    
    sm2 = plt.cm.ScalarMappable(cmap=plt.cm.Oranges, norm=plt.Normalize(vmin=min(node_colors2), vmax=max(node_colors2)))
    sm2.set_array([])

    
    # Add labels
    labels1 = {node: f"$\\bf{{{G.nodes[node]['stock_price']:.2f}}}$" for node in G.nodes()}
    labels2 = {node: f"$\\bf{{{G.nodes[node]['option_value']:.2f}}}$" for node in G.nodes()}
    
    nx.draw_networkx_labels(G, pos, labels=labels1, ax=ax1, font_size=8)
    nx.draw_networkx_labels(G, pos, labels=labels2, ax=ax2, font_size=8)
    
    # Remove axes
    ax1.set_axis_off()
    ax2.set_axis_off()
    
    plt.tight_layout()
    plt.show()
