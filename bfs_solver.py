import numpy as np
import time

from n_puzzle_base import NPuzzleBase
from loguru import logger

logger.add('logger_puzzle.log')


class Node:
    def __init__(self, node_no, data, parent, act):
        self.node_no = node_no
        self.data = data
        self.parent = parent
        self.act = act


class BFSSolver(NPuzzleBase):
    @classmethod
    def move_tile(cls, action, data):
        if action == 'up':
            return cls.move_up(data)
        if action == 'down':
            return cls.move_down(data)
        if action == 'left':
            return cls.move_left(data)
        if action == 'right':
            return cls.move_right(data)
        else:
            return None

    def solve(self, node):
        logger.debug("Solucionando...")
        actions = ["down", "up", "left", "right"]
        goal_node = self.target_matrix
        node_q = [node]
        final_nodes = []
        visited = []

        # Only writing data of nodes in seen
        final_nodes.append(node_q[0].data.tolist())
        node_counter = 0  # To define a unique ID to all the nodes formed

        while node_q:
            current_root = node_q.pop(0)  # Pop the element 0 from the list
            if current_root.data.tolist() == goal_node.tolist():
                logger.success("Problema solucionado.")
                return current_root, final_nodes, visited

            for move in actions:
                temp_data = self.move_tile(move, current_root.data)
                if temp_data is not None:
                    node_counter += 1
                    child_node = Node(node_counter, np.array(temp_data),
                                      current_root, move)  # Create a child node

                    if child_node.data.tolist() not in final_nodes:
                        node_q.append(child_node)
                        # Add the child node data in final node list
                        final_nodes.append(child_node.data.tolist())
                        visited.append(child_node)
                        if child_node.data.tolist() == goal_node.tolist():
                            logger.success("Problema solucionado.")
                            return child_node, final_nodes, visited
        return None, None, None  # return statement if the goal node is not reached


if __name__ == '__main__':
    n = 8
    logger.info(f"Iniciando {n}-Puzzle")

    bfs = BFSSolver(n)
    matrix = bfs.matrix
    logger.debug(f"Matriz de entrada: \n{matrix}")

    if bfs.check_both_conditions():
        root = Node(0, matrix, None, None)
        start = time.time()
        goal, f_nodes, visited_nodes = bfs.solve(root)
        end = time.time()
        if goal:
            logger.info(f"Tempo: {end - start} segundos.")
            logger.info(f"Resultado: \n{goal.data}")
