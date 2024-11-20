import pandas as pd
import networkx as nx
import streamlit as st
import pyvis_network as Network

connections = pd.read_csv("Connections.csv")
classes = pd.read_csv("Classes.csv")
G = nx.DiGraph()

for i in connections.index:
    G.add_edge(connections.loc[i, "Source"], connections.loc[i, "Target"], weight=connections.loc[i, "Weight"])



st.title("Alpha Epsilon Zeta Family Tree")
st.write("Visualize the shortest path between members in the family tree with weighted edges.")

# Input for selecting start and end members
members = set(connections['Source'])
start_member = st.selectbox("Select Start Member", list(members))
end_member = st.selectbox("Select End Member", list(members))

# Find and display the shortest path
if st.button("Find Shortest Path"):
    if nx.has_path(G, start_member, end_member):
        shortest_path = nx.shortest_path(G, start_member, end_member, weight='weight')
        st.write(f"Shortest path from {start_member} to {end_member} with weights:")
        st.write(" → ".join(shortest_path))

        # Visualization of the graph with highlighted path
        net = Network(height="500px", width="100%", notebook=False)
        for node in G.nodes:
            net.add_node(node, color="lightblue" if node not in shortest_path else "orange")
        for edge in G.edges(data=True):
            color = "orange" if (edge[0] in shortest_path and edge[1] in shortest_path) else "gray"
            weight = edge[2]['weight']
            net.add_edge(edge[0], edge[1], color=color, label=str(weight), width=weight)

        # Display the network
        net.show("family_tree.html")
        st.write("### Family Tree Visualization with Weights")
        st.components.v1.html(open("family_tree.html", "r").read(), height=550)
    else:
        st.write("No path exists between the selected members.")




