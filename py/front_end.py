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

        nodes = self.dbhandler.database['nodes']
        
        self.dropdown_options1 = tk.StringVar(self.root)
        self.dropdown_options1.set("parent") # default value
        self.dropdown_options2 = tk.StringVar(self.root)
        self.dropdown_options2.set("child") # default value

        self.dropdown_options3 = tk.StringVar(self.root)
        self.dropdown_options3.set("parent") # default value
        self.dropdown_options4 = tk.StringVar(self.root)
        self.dropdown_options4.set("child") # default value

        if len(nodes) < 1:
            self.drowdown1 = tk.OptionMenu(self.root, self.dropdown_options1 , value = '')
            self.drowdown2 = tk.OptionMenu(self.root, self.dropdown_options2, value = '')
            self.drowdown3 = tk.OptionMenu(self.root, self.dropdown_options3 , value = '')
            self.drowdown4 = tk.OptionMenu(self.root, self.dropdown_options2, value = '')
        else:
            self.drowdown1 = tk.OptionMenu(self.root, self.dropdown_options1, *nodes)
            self.drowdown2 = tk.OptionMenu(self.root, self.dropdown_options2, *nodes)
            self.drowdown3 = tk.OptionMenu(self.root, self.dropdown_options3, *nodes)
            self.drowdown4 = tk.OptionMenu(self.root, self.dropdown_options4, *nodes)
   
        self.drowdown1.config(width=8, height=1)
        self.drowdown2.config(width=8, height=1)
        self.drowdown1.grid(column=1, row=1, padx = 32, pady=10)
        self.drowdown2.grid(column=2, row=1, pady=10)

        self.drowdown3.config(width=8, height=1)
        self.drowdown4.config(width=8, height=1)
        self.drowdown3.grid(column=1, row=3, padx = 32, pady=10)
        self.drowdown4.grid(column=2, row=3, pady=10)

        self.add_node_box = tk.Text(self.root, height=1, width=30)
        self.add_node_box.grid(column=1, row=0, pady=10, columnspan=2)

        self.delete_node_box = tk.Text(self.root, height=1, width=30)
        self.delete_node_box.grid(column=1, row=2, pady=10, columnspan=2)

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

        self.visualize()

    def update_option_menu(self):

        menu1 = self.drowdown1["menu"]
        menu1.delete(0, "end")
        menu2 = self.drowdown2["menu"]
        menu2.delete(0, "end")
        menu3 = self.drowdown3["menu"]
        menu3.delete(0, "end")
        menu4 = self.drowdown4["menu"]
        menu4.delete(0, "end")

        for string in self.dbhandler.database['nodes']:
            menu1.add_command(label=string, 
                             command=lambda value=string: self.dropdown_options1.set(value))
            menu2.add_command(label=string, 
                             command=lambda value=string: self.dropdown_options2.set(value))
            menu3.add_command(label=string, 
                             command=lambda value=string: self.dropdown_options3.set(value))
            menu4.add_command(label=string, 
                             command=lambda value=string: self.dropdown_options4.set(value))
        
            
            
            
    def add_node(self):
        """ adding a node in the database if it doesnt exist
        """
        if len(self.add_node_box.get("1.0", "end-1c")) == 0:
            print("Textbox empty")
            return
        else:
            self.dbhandler.add_node(self.add_node_box.get("1.0", "end-1c"))
        
        self.update_option_menu()
        self.visualize()

    def add_edge(self):
        """ adding a edge in the database if it doesnt exist
        """
        if self.dropdown_options1.get() == 'parent' or self.dropdown_options2.get() == 'child':
            print ("node not found in database")
            return
        else:
            nodes = self.dropdown_options1.get()
            nodes = nodes + ',' + self.dropdown_options2.get()
            self.dbhandler.add_edge(nodes)
        self.visualize()

    def delete_node(self):
        """ deleting a node in the database if it exists
        """
        if len(self.delete_node_box.get("1.0", "end-1c")) == 0:
            print("Textbox empty")
            return
        else:
            self.dbhandler.delete_node(
                self.delete_node_box.get("1.0", "end-1c"))
        self.update_option_menu()
        self.visualize()

    def delete_edge(self):
        """ deleting a edge in the database if it exists
        """
        if self.dropdown_options3.get() not in self.dbhandler.database['nodes'] or self.dropdown_options4.get() not in self.dbhandler.database['nodes']:
            print ("node not found in database")
            return
        else:
            nodes = self.dropdown_options3.get()
            nodes = nodes + ',' + self.dropdown_options4.get()
            edge_deleted = self.dbhandler.delete_edge(nodes)
            if not edge_deleted:
                return

        self.visualize()

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
        plt.clf()
        self.reload_nodes()
        nx.draw(self.graph, with_labels=True)
        plt.show()
