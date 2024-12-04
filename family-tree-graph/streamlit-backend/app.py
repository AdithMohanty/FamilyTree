import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

base_dir = os.path.dirname(__file__)

connections_file = os.path.join(base_dir, "Connections.csv")
names_and_weights_file = os.path.join(base_dir, "NamesAndWeights.csv")
graph_output_file = os.path.join(base_dir, "interactive_graph.html")

connections = pd.read_csv(connections_file)

G = nx.DiGraph()
for i in connections.index:
    G.add_edge(connections.loc[i, "Source"], connections.loc[i, "Target"], weight=int(connections.loc[i, "Weight"]))

def find_shortest_path(source, target):
    try:
        path = nx.shortest_path(G, source=source, target=target, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None

def visualize_graph():
    net = Network(height="750px", width="100%", font_color="white", bgcolor="#222222", notebook=True, filter_menu=True, cdn_resources="remote")
    net.from_nx(G)

    net.set_options("""
    var options = {
      "nodes": {
        "color": {
          "border": "rgba(0,102,204,1)",
          "background": "rgba(102,178,255,1)",
          "highlight": {
            "border": "rgba(255,51,51,1)",
            "background": "rgba(255,153,153,1)"
          }
        }
      },
      "edges": {
        "color": {
          "color": "rgba(102,102,102,0.8)"
        },
        "arrows": {
          "to": { "enabled": true }
        }
      },
      "physics": {
        "enabled": true
      }
    }
    """)

    net.show(graph_output_file)
    return graph_output_file

def find_shortest_path_length(source, target):
    path = find_shortest_path(source, target)
    length = 0

    allNames = pd.read_csv(names_and_weights_file)
    weights = {}
    for i in range(len(allNames)):
      weights[allNames.loc[i, "Full Name"]] = int(allNames.loc[i, "Weight"])

    for i in path:
        length += weights[i]
    return length
    
st.title('The Organization Graph')

source = st.selectbox('Enter the source family member', G.nodes())
target = st.selectbox('Enter the target family member', G.nodes())

if source and target:
    path = find_shortest_path(source, target)
    path_length = find_shortest_path_length(source, target)
    if path:
        st.write(f"The shortest path from {source} to {target} is:")
        st.write(" -> ".join(path))
        st.write(f"The length of the shortest path is {path_length}")
    else:
        st.write(f"No path found between {source} and {target}")

st.markdown("### Family Tree Visualization")
st.components.v1.html(open(graph_output_file, "r").read(), height=750)
