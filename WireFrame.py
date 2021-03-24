import math
import numpy as np

class WireFrame:
	def __init__(self):
		self.nodes = np.zeros((0, 4))
		self.edges = []
		self.faces = []
		self.colors = []

	def addColors(self, colors):
		self.colors += colors

	def addNodes(self, node_array):
		ones_column = np.ones((len(node_array), 1))
		ones_added = np.hstack((node_array, ones_column))
		self.nodes = np.vstack((self.nodes, ones_added))

	def addEdges(self, edges):
		self.edges += edges

	def addFaces(self, faces):
		self.faces += faces

	def transform(self, matrix):
		self.nodes = np.dot(self.nodes, matrix)

	def translationMatrix(self, dx = 0, dy = 0, dz = 0):
		return np.array([[1, 0, 0, 0],
						 [0, 1, 0, 0],
						 [0, 0, 1, 0],
						 [dx, dy, dz, 1]])

	def scaleMatrix(self, s, cx = 0, cy = 0, cz = 0):
		return np.array([[s, 0, 0, 0],
						 [0, s, 0, 0],
						 [0, 0, s, 0],
						 [cx * (1 - s), cy * (1 - s), cz * (s - 1), 1]])

	def rotateXMatrix(self, radians):
		c = np.cos(radians)
		s = np.sin(radians)

		return np.array([[1, 0, 0, 0],
						 [0, c, -s, 0],
						 [0, s, c, 0],
						 [0, 0, 0, 1]])

	def rotateYMatrix(self, radians):
		c = np.cos(radians)
		s = np.sin(radians)

		return np.array([[c, 0, s, 0],
						 [0, 1, 0, 0],
						 [-s, 0, c, 0],
						 [0, 0, 0, 1]])

	def rotateZMatrix(self, radians):
		c = np.cos(radians)
		s = np.sin(radians)

		return np.array([[c, -s, 0, 0],
						 [s, c, 0, 0],
						 [0, 0, 1, 0],
						 [0, 0, 0, 1]])

	def findCenter(self):
		min_values = self.nodes[:,:-1].min(axis = 0)
		max_values = self.nodes[:,:-1].max(axis = 0)

		return 0.5 * (min_values + max_values)

	#################### DEBUG ####################

	def _outputNodes(self):
		print("\n --- Nodes ---")

		for i, (x, y, z, _) in enumerate(self.nodes):
			print(f"{i}: {x}, {y}, {z}")

	def _outputEdges(self):
		print("\n --- Edges ---")

		for i, (node1, node2) in enumerate(self.edges):
			print(f"{i}: {node1} -> {node2}")

	def _outputFaces(self):
		print("\n --- Faces ---")

		for i in range(len(self.faces)):
			print(f"{i}: {self.faces[i]}")
