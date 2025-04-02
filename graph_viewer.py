import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from kmvm_core import kmvm_graph

def show_kmvm_graph():
    st.subheader("🧠 Hamlet's Mind Map")

    G = kmvm_graph.get_graph()
    if not G.nodes:
        st.info("Graph is empty.")
        return

    pos = nx.spring_layout(G)
    labels = {node: G.nodes[node]["kmvm"]["motive"] for node in G.nodes}

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='skyblue', node_size=1500, font_size=10)
    st.pyplot(plt)
