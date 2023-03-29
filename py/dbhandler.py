import os
import json


class GraphDB:
    """Database manager for the graph visualizer tool
    """

    def __init__(self, data_path: str):

        self.dbpath = data_path
        if os.path.exists(self.dbpath):
            with open(self.dbpath, 'r', encoding='utf-8') as file:
                self.database = json.load(file)
        else:
            self.database = {}
            self.database['nodes'] = []
            self.database['edges'] = []

    def add_node(self, node: str):
        """adding a node in the database

        Args:
            node (str): The name of the node
        """
        node = node.strip()
        if node not in self.database['nodes']:
            self.database['nodes'].append(node)
        else:
            print("Node already in the database")
        self.save_data()

    def delete_node(self, node: str):
        """deleting a node from the database

        Args:
            node (str): The name of the node
        """
        node = node.strip()
        node_found = False
        num_edges = len(self.database['edges'])
        remove_edges = []
        for i in range(num_edges):
            if node in self.database['edges'][i].split(','):
                remove_edges.append(self.database['edges'][i])
                node_found = True
        for edge in remove_edges:
            self.database['edges'].remove(edge)

        if node in self.database['nodes']:
            self.database['nodes'].remove(node)
            node_found = True

        if node_found is False:
            print("Node not in the database")
        self.save_data()

    def add_edge(self, nodes: str):
        """adding an edge in the database

        Args:
            nodes (str): The two nodes seperated by a , and possiblty a space
        """

        nodes_arr = nodes.split(',')
        nodes_arr[0] = nodes_arr[0].strip()
        nodes_arr[1] = nodes_arr[1].strip()
        nodes = nodes_arr[0] + ',' + nodes_arr[1]
        if nodes in self.database['edges']:
            print("Edge already in the database")
        else:
            self.database['edges'].append(nodes)
        self.save_data()

    def delete_edge(self, nodes: str):
        """deleting an edge in the database

        Args:
           nodes (str): The two nodes seperated by a , and possiblty a space
        """
        nodes_arr = nodes.split(',')
        nodes_arr[0] = nodes_arr[0].strip()
        nodes_arr[1] = nodes_arr[1].strip()
        nodes = nodes_arr[0] + ',' + nodes_arr[1]
        if nodes in self.database['edges']:
            self.database['edges'].remove(nodes)
        else:
            print("Edge not found in the database")
        self.save_data()

    def save_data(self):
        """Saving database in database.json file
        """

        with open(self.dbpath, 'w', encoding='utf-8') as file:
            json.dump(self.database, file)
