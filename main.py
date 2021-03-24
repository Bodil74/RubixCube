from WireFrame import WireFrame
from Projection import ProjectionViewer
import numpy as np
import random
import pygame
import time

pygame.init()

rubix_nodes = [(x, y, z) for x in (210, 266, 333, 400) for y in (210, 266, 333, 400) for z in (210, 266, 333, 400)]

rubix = WireFrame()
rubix.addNodes(np.array(rubix_nodes))

rubix.addFaces([[n, n + 16, n + 20, n + 4] for n in (0, 4, 8, 16, 20, 24, 32, 36, 40, 3, 7, 11, 19, 23, 27, 35, 39, 43)])
rubix.addFaces([[n, n + 16, n + 17, n + 1] for n in (12, 13, 14, 28, 29, 30, 44, 45, 46, 0, 1, 2, 16, 17, 18, 32, 33, 34)])
rubix.addFaces([[n, n + 1, n + 5, n + 4] for n in (0, 4, 8, 1, 5, 9, 2, 6, 10, 48, 52, 56, 49, 53, 57, 50, 54, 58)])

#rubix.addColors((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for n in range(54))

rubix.addColors([(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0),
				(255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0),
				(0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0),
				(255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0),
				(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
				(0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255)])

pv = ProjectionViewer(600, 600)
pv.addWireFrame('rubix', rubix)


class Help:
	def __init__(self):
		self.font = pygame.font.SysFont('arial', 30)
		self.text = self.font.render('Help', True, (255, 255, 255))
		self.rect = pygame.Rect(535, 10, 51, 35)

	def draw(self):
		pv.screen.blit(self.text, (535, 10))

	def on_click(self):
		opened = True
		menu_rect = pygame.Rect(100, 50, 400, 500)
		menu_text = pygame.image.load('./images/help_menu.png')

		while opened:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					opened = False
					pygame.quit()
					exit()

				elif event.type == pygame.MOUSEBUTTONUP:
					if not pygame.Rect.collidepoint(menu_rect, pygame.mouse.get_pos()):
						opened = False

			pygame.draw.rect(pv.screen, (48, 48, 48), menu_rect)
			pv.screen.blit(menu_text, (100, 100))
			pygame.draw.rect(pv.screen, (255, 255, 255), menu_rect, 1)

			pygame.display.flip()


class Timer():
	def __init__(self):
		pass


def rotate_side(side, color_copy):
	cells = [i for i in range(side, side + 9)]
	twod_cells = [[cells[n], cells[n + 1], cells[n + 2]] for n in (0, 3, 6)]
	rotated_cells = list(zip(*reversed(twod_cells)))

	if side == 0 or side == 9:
		x = twod_cells
		twod_cells = rotated_cells
		rotated_cells = x

	for i in range(len(twod_cells)):
		for j, k in enumerate(twod_cells[i]):
			rubix.colors[k] = color_copy[rotated_cells[i][j]] 

def rotate(cells, side = -1):
	color_copy = rubix.colors.copy()
	shifted_cells = list(cells)

	for i in range(3):
		shifted_cells.insert(0, shifted_cells.pop(-1))

	for i, j in enumerate(shifted_cells):
		rubix.colors[j] = color_copy[cells[i]]

	if side > -1:
		rotate_side(side, color_copy)

def scramble():
	pass

def draw():
	pv.display()
	help_button.draw()

	pygame.display.flip()

def main():

	pv.current_wireframe = pv.wireframes['rubix']

	pv.rotateAll('X', 0.78)
	pv.rotateAll('Y', 0.60)
	pv.rotateAll('Z', 0.51)
	pv.translateAll([-15, 0, 0])
	pv.translateAll([0, -10, 0])

	running = True
	key_to_function = {pygame.K_EQUALS : (lambda x : x.scaleAll(1.25)),
					   pygame.K_MINUS : (lambda x : x.scaleAll(0.8)),
					   pygame.K_q : (lambda x : x.rotateAll('X', 0.1)),
					   pygame.K_w : (lambda x : x.rotateAll('X', -0.1)),
					   pygame.K_a : (lambda x : x.rotateAll('Y', 0.1)),
					   pygame.K_s : (lambda x : x.rotateAll('Y', -0.1)),
					   pygame.K_z : (lambda x : x.rotateAll('Z', 0.1)),
					   pygame.K_x : (lambda x : x.rotateAll('Z', -0.1)),
					   pygame.K_1 : (lambda x : rotate((33, 30, 27, 36, 37, 38, 18, 21, 24, 47, 46, 45), 0)),
					   pygame.K_2 : (lambda x : rotate((34, 31, 28, 39, 40, 41, 19, 22, 25, 50, 49, 48))),
					   pygame.K_3 : (lambda x : rotate((35, 32, 29, 42, 43, 44, 20, 23, 26, 53, 52, 51), 9)),
					   pygame.K_4 : (lambda x : rotate((2, 5, 8, 47, 50, 53, 17, 14, 11, 44, 41, 38), 18)),
					   pygame.K_5 : (lambda x : rotate((1, 4, 7, 46, 49, 52, 16, 13, 10, 43, 40, 37))),
					   pygame.K_6 : (lambda x : rotate((0, 3, 6, 45, 48, 51, 15, 12, 9, 42, 39, 36), 27)),
					   pygame.K_7 : (lambda x : rotate((2, 1, 0, 27, 28, 29, 9, 10, 11, 20, 19, 18), 36)),
					   pygame.K_8 : (lambda x : rotate((5, 4, 3, 30, 31, 32, 12, 13, 14, 27, 22, 21))),
					   pygame.K_9 : (lambda x : rotate((8, 7, 6, 33, 34, 35, 15, 16, 17, 26, 25, 24), 45))}

	while running:

		draw()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			elif event.type == pygame.KEYDOWN:
				if pv.current_wireframe != False:
					if event.key in key_to_function:
						key_to_function[event.key](pv)

			elif event.type == pygame.MOUSEBUTTONUP:
				if pygame.Rect.collidepoint(help_button.rect, pygame.mouse.get_pos()):
					help_button.on_click()

help_button = Help()
main()
