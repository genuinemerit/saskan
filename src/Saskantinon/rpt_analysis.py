#!python
"""
:module:    io_analysis.py
:author:    GM (genuinemerit @ pm.me)
Saskan Admin Report Generator

@DEV:
- Consider whether it makes sense to move other
  reporting functions to this module.
"""

from pprint import pprint as pp  # noqa: F401

import matplotlib.pyplot as plt  # type: ignore
import networkx as nx  # type: ignore


class Analysis(object):
    """Provide report and monitoring methods."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the object.
        """
        pass

    # System monitoring reports
    def rpt_ufw_status(self):
        """Get UFW status."""
        ok, result = self.run_cmd("ufw status numbered")
        if ok:
            return result

    # Graph data functions
    def get_ntype(self, p_N: dict, p_node_nm: str):
        """Return node type for a given node name.

        :args:
        - p_N (dict): additional nodes metadata for graph object
        - p_title (str): Name of a schema/ontology, e.g. "scenes"
        - p_node_nm (str): Node name.
        """
        node_type = None
        for nt, nodes in p_N["name"].items():
            if p_node_nm in nodes:
                node_type = nt
                break
        return node_type

    def set_graph(self, p_E: dict, p_incl_nodes: list = []):
        """Populate networkx graph dataset using edges dataset.
        - Defining the edges automatically also defines the nodes.
        - Limiting the graph to a subset of nodes here affects what
          is reported and displayed by report and display functions.
        - If no subset is defined, all nodes are included.

        :args:
        - p_E (dict): Edge data for graph object
        - p_incl_nodes (list): Node names to include in graph (optional)
        """
        G = nx.MultiDiGraph()
        for e_list in p_E["name"].values():
            edges = list()
            for n1, n2 in e_list:
                if p_incl_nodes == []:
                    edges.append(tuple((n1, n2)))
                elif n1 in p_incl_nodes or n2 in p_incl_nodes:
                    edges.append(tuple((n1, n2)))
            G.add_edges_from(edges)
        return G

    def get_nodes_in_type(self, p_N: dict, p_type_nm: str):
        """Return list of nodes in a given node type.

        :args:
        - p_N (dict): additional nodes metadata for graph object
        - p_title (str): Name of a schema/ontology, e.g. "scenes"
        - p_node_nm (str): Node name.
        """
        nodes = []
        if p_type_nm in p_N["name"]:
            nodes = p_N["name"][p_type_nm]
        return {p_type_nm: nodes}

    def get_edges_for_nodes(self, p_E: dict, p_edge_nm: tuple, p_node_vals: list):
        """List all nodes in a given edge for the set of
        rqeuested node values. It is assumed that the node value list
        is associated with node name 1.

        :args:
        - p_E (dict): additional edge metadata for graph object
        - p_edge_nm (tuple): (node name 1, node name 2)
        - p_node_vals (list): list of node values for node name 1
        """
        # pp((p_E))
        # print(f"p_edge_nm: {p_edge_nm}")
        reverse_edge = False
        nodes_d: dict = {}
        if p_edge_nm not in p_E["types"]:
            reverse_edge = True
            p_edge_nm = tuple(reversed(p_edge_nm))
        if p_edge_nm in p_E["types"]:
            if reverse_edge:
                nodes = sorted(
                    [tuple(reversed(edge)) for edge in p_E["name"][p_edge_nm]]
                )
            else:
                nodes = p_E["name"][p_edge_nm]
            nodes = [n for n in nodes if n[0] in p_node_vals]
            for n in nodes:
                if n[0] not in nodes_d.keys():
                    nodes_d[n[0]] = []
                nodes_d[n[0]].append(n[1])
        return nodes_d

    def get_degrees(self, p_set_nm: str, p_G, p_N: dict):
        """Show report of degrees for graphed nodes.

        :args:
        - p_set_nm (str): Name of the graph set
        - p_G (nx.MultiDiGraph()): networkx graph object
        - p_N (dict): additional node metadata for graph object

        @DEV:
        - Integrate Analysis() into the admin app
        - Provide interactive options and reports like:
            - List all nodes, be able to pick a subset
            - List node-type and edge-type, be able to pick subset
            - List scenes on a timeline,
                optionally list selected nodes in each scene
        - Do NOT try to create an editor for the JSON file,
            just use a fucking editor. :-)
        - Parameterize report options
        """
        rpt_data = sorted(
            [(p_G.degree(n), n, self.get_ntype(p_N, n)) for n in p_G.nodes()],
            reverse=True,
        )
        return {f"degrees for {p_set_nm}": rpt_data}

    def draw_graph(self, p_title: str, p_G, p_N: dict, p_E: dict):
        """Draw graph based on G data.

        :args:
        - p_title (str): name of the graph set
        - p_G (nx.MultiDiGraph()): networkx graph object
        - p_N (dict): additional node metadata for graph object
        - p_E (dict): additional edge metadata for graph object
        """
        node_sizes = [p_G.degree(n) * 23 for n in p_G.nodes()]
        node_labels = {n: f"\n{self.get_ntype(p_N, n)}\n{n}" for n in p_G.nodes()}
        node_colors = [p_N["color"][n] for n in p_G.nodes()]
        edge_colors = [
            p_E["color"][
                (self.get_ntype(p_N, e[0]), self.get_ntype(p_N, e[1]))
            ].replace("0", "5")
            for e in p_G.edges()
        ]
        # Folks online tend to recommend graphviz for drawing graphs, but
        # I could not get graphviz to work with my environment, networkx.

        # See: https://networkx.org/documentation/stable/reference/drawing.html

        # Most of these layouts need or require additional parameters,
        #  but I am not clear yet on how to set them usefully.

        # Ones I prefer so far are marked with a "# *" comment.
        pos = nx.spiral_layout(p_G)  # *
        # pos = nx.spring_layout(G, seed=13648)     # *
        # pos = nx.circular_layout(G)               # *
        # pos = nx.shell_layout(G)                  # *
        # pos = nx.kamada_kawai_layout(G)           # requires scipy
        # pos = nx.random_layout(G)
        # pos = nx.spectral_layout(G)
        plt.title(p_title)
        cmap = plt.cm.plasma
        ax = plt.gca()
        ax.set_axis_off()
        nx.draw_networkx_nodes(
            p_G, pos, linewidths=1, node_color=node_colors, node_size=node_sizes
        )
        nx.draw_networkx_edges(
            p_G, pos, arrows=False, edge_color=edge_colors, edge_cmap=cmap, width=1
        )
        # Node labels
        nx.draw_networkx_labels(
            p_G,
            pos,
            font_size=9,
            font_color="indigo",
            labels=node_labels,
            verticalalignment="top",
        )
        plt.show()
