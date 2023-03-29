import os
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from IPython.display import clear_output
from py.process_graph import hierarchy_pos
from py.dbhandler import GraphDB


class GUI:
    """The GUI class that creates the front end of our graph visualizer
    """

    def __init__(self, data_path: str):
        self.root = tk.Tk()
        self.dbhandler = GraphDB(os.path.join(data_path, 'db.json'))
        self.root.geometry("600x600")
        self.root.title("Graph-Visualizer")
        self.graph = nx.DiGraph()
        self.create_front_page()
        self.root.mainloop()

    def create_front_page(self):
        """Creating the front/index page including all the text boxes and buttons
        """
        tk.Label(self.root, text="Add Node", font=(
            'Arial', 14)).grid(column=0, row=0, pady=10)

        tk.Label(self.root, text="Add Edge", font=(
            'Arial', 14)).grid(column=0, row=1, pady=10)

        tk.Label(self.root, text="Delete Node", font=(
            'Arial', 14)).grid(column=0, row=2, pady=10)

        tk.Label(self.root, text="Delete Edge", font=(
            'Arial', 14)).grid(column=0, row=3, pady=10)

        self.root_node = ''
        self.add_node_box = tk.Text(self.root, height=1, width=30)
        self.add_node_box.grid(column=1, row=0, pady=10, columnspan=2)

        self.add_edge_box = tk.Text(self.root, height=1, width=30)
        self.add_edge_box.grid(column=1, row=1, pady=10, columnspan=2)

        self.delete_node_box = tk.Text(self.root, height=1, width=30)
        self.delete_node_box.grid(column=1, row=2, pady=10, columnspan=2)

        self.delete_edge_box = tk.Text(self.root, height=1, width=30)
        self.delete_edge_box.grid(column=1, row=3, pady=10, columnspan=2)

        self.button = tk.Button(self.root, text="Add Node", font=(
            'Arial', 14), height=1, width=14, command=self.add_node)
        self.button.grid(column=3, row=0, pady=10)

        self.button = tk.Button(self.root, text="Add Edge", font=(
            'Arial', 14), height=1, width=14, command=self.add_edge)
        self.button.grid(column=3, row=1, pady=10)

        self.button = tk.Button(self.root, text="Delete Node", font=(
            'Arial', 14), height=1, width=14, command=self.delete_node)
        self.button.grid(column=3, row=2, pady=10)

        self.button = tk.Button(self.root, text="Delete Edge", font=(
            'Arial', 14), height=1, width=14, command=self.delete_edge)
        self.button.grid(column=3, row=3, pady=10)

        self.button = tk.Button(self.root, text="Visualize Graph", font=(
            'Arial', 14), height=1, width=14, command=self.visualize)
        self.button.grid(column=2, row=4, pady=10)

    def add_node(self):
        """ adding a node in the database if it doesnt exist
        """
        if len(self.add_node_box.get("1.0", "end-1c")) == 0:
            print("Textbox empty")
        else:
            self.dbhandler.add_node(self.add_node_box.get("1.0", "end-1c"))

    def add_edge(self):
        """ adding a edge in the database if it doesnt exist
        """
        if len(self.add_edge_box.get("1.0", "end-1c")) == 0:
            print("Textbox empty")
        elif ',' not in self.add_edge_box.get("1.0", "end-1c"):
            print(
                "there is only 1 node, please seperate nodes by putting a comma(,) in between")
        else:
            nodes = self.add_edge_box.get("1.0", "end-1c")
            self.dbhandler.add_edge(nodes)

    def delete_node(self):
        """ deleting a node in the database if it exists
        """
        if len(self.delete_node_box.get("1.0", "end-1c")) == 0:
            print("Textbox empty")
        else:
            self.dbhandler.delete_node(
                self.delete_node_box.get("1.0", "end-1c"))

    def delete_edge(self):
        """ deleting a edge in the database if it exists
        """
        if len(self.delete_edge_box.get("1.0", "end-1c")) == 0:
            print("Textbox empty")
        elif ',' not in self.delete_edge_box.get("1.0", "end-1c"):
            print(
                "there is only 1 node, please seperate nodes by putting a comma(,) in between")
        else:
            nodes = self.delete_edge_box.get("1.0", "end-1c")
            self.dbhandler.delete_edge(nodes)

    def reload_nodes(self):
        """ reload all the nodes from dbhandler
        """
        self.graph = nx.DiGraph()
        for node in self.dbhandler.database['nodes']:
            self.graph.add_node(node)
        for edge in self.dbhandler.database['edges']:
            nodes = edge.split(',')
            self.graph.add_edge(nodes[0], nodes[1])

    def visualize_tree(self):
        """ Visualize the graph in a tree like format
        """
        clear_output(wait=True)
        self.reload_nodes()
        pos = hierarchy_pos(self.graph, 'Tree')
        nx.draw(self.graph, pos=pos, with_labels=True)

    def visualize(self):
        """ Visualize the graph
        """
        clear_output(wait=True)
        self.reload_nodes()
        nx.draw(self.graph, with_labels=True)
        plt.show()
