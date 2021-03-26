
import pygame
import numpy as np
import time

pygame.init()

def common_data(list1, list2):
	for i in list1:
		for j in list2:
			if i == j:
				return True

	return False

def sort_nodes(li, nodes_z):
	x = []

	for i in li:
	    x.append(nodes_z.index(i))

	return x

class ProjectionViewer:
	def __init__(self, width = 300, height = 300, title = '3D-Viewer'):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)
		self.background = (0, 0, 0)
		self.wireframes = {}
		self.displayNodes = False
		self.displayEdges = False
		self.displayFaces = True
		self.displayFPS = True
		self.nodeColor = (255, 255, 255)
		self.edgeColor = (255, 255, 255)
		self.nodeRadius = 4

		self.current_wireframe = None

		self.font = pygame.font.SysFont("arial", 18)
		self.start = time.time()
		self.current = self.start
		self.counter = 0
		self.text_surface = self.font.render(str(self.counter), True, (255, 255, 255))
		self.text_rect = self.text_surface.get_rect()

	def addWireFrame(self, name, wireframe):
		self.wireframes[name] = wireframe

	def display(self):
		self.screen.fill(self.background)

		for wireframe in self.wireframes.values():
			display_edges = wireframe.edges.copy()
			
			if self.displayFaces:

				wireframe_nodes = wireframe.nodes.copy().tolist()
				wireframe_nodes.sort(reverse = True, key = lambda x : x[2])

				faces = wireframe.faces.copy()

				ordered_nodes = wireframe.nodes[:, 2].tolist()
				ordered_nodes = sort_nodes(sorted(ordered_nodes), ordered_nodes)

				for node in ordered_nodes[::-1]:
					for ii, face in enumerate(faces):
						if node in face:
							pygame.draw.polygon(self.screen, wireframe.colors[ii], tuple(map(tuple, (wireframe.nodes[i][:2] for i in face))))

			if self.displayEdges:
				for n1, n2 in display_edges:
					pygame.draw.aaline(self.screen, self.edgeColor, wireframe.nodes[n1][:2], wireframe.nodes[n2][:2], 1)

			if self.displayNodes:
				for node in wireframe.nodes:
					pygame.draw.circle(self.screen, self.nodeColor, (int(node[0]), int(node[1])), self.nodeRadius, 0)

			if self.displayFPS:
				if self.current - self.start > 1:
					self.start = self.current
					self.text_surface = self.font.render(str(self.counter), True, (255, 255, 255))
					self.text_rect = self.text_surface.get_rect()
					self.counter = 0

				else:
					self.current = time.time()
					self.counter += 1

				self.screen.blit(self.text_surface, self.text_rect)

	def translateAll(self, vector):
		wireframe = self.current_wireframe

		matrix = wireframe.translationMatrix(*vector)
		wireframe.transform(matrix)

	def scaleAll(self, scale):
		wireframe = self.current_wireframe

		center_x = self.width / 2
		center_y = self.height / 2

		scale_matrix = wireframe.scaleMatrix(scale, center_x, center_y, 0)
		wireframe.transform(scale_matrix)

	def rotateAll(self, axis, radians):
		rotateFunction = 'rotate' + axis + 'Matrix'
		wireframe = self.current_wireframe

		(x, y, z) = wireframe.findCenter()
		translation_matrix1 = wireframe.translationMatrix(-x, -y, -z)
		translation_matrix2 = wireframe.translationMatrix(x, y, z)

		rotation_matrix = getattr(wireframe, rotateFunction)(radians)
		rotation_matrix = np.dot(np.dot(translation_matrix1, rotation_matrix), translation_matrix2)
		wireframe.transform(rotation_matrix)

	def run(self, func):
		self.current_wireframe = self.wireframes['rubix']
		running = True
		key_to_function = {pygame.K_LEFT : (lambda x : x.translateAll([-10, 0, 0])),
						   pygame.K_RIGHT : (lambda x : x.translateAll([10, 0, 0])),
						   pygame.K_DOWN : (lambda x : x.translateAll([0, 10, 0])),
						   pygame.K_UP : (lambda x : x.translateAll([0, -10, 0])),
						   pygame.K_EQUALS : (lambda x : x.scaleAll(1.25)),
						   pygame.K_MINUS : (lambda x : x.scaleAll(0.8)),
						   pygame.K_q : (lambda x : x.rotateAll('X', 0.1)),
						   pygame.K_w : (lambda x : x.rotateAll('X', -0.1)),
						   pygame.K_a : (lambda x : x.rotateAll('Y', 0.1)),
						   pygame.K_s : (lambda x : x.rotateAll('Y', -0.1)),
						   pygame.K_z : (lambda x : x.rotateAll('Z', 0.1)),
						   pygame.K_x : (lambda x : x.rotateAll('Z', -0.1)),}

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				elif event.type == pygame.KEYDOWN:
					if self.current_wireframe != False:
						if event.key in key_to_function:
							key_to_function[event.key](self)

			self.display()
			pygame.display.flip()
