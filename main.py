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
			pv.screen.blit(menu_text, (100, 50))
			pygame.draw.rect(pv.screen, (255, 255, 255), menu_rect, 1)

			pygame.display.flip()


def rotate_side():
	pass

def rotate_middle():
	
	for i in (1, 4, 7, 37, 40, 43, 16, 13, 10, 50, 49, 48):
		rubix.colors[i] = (48, 48, 48)

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

	rotate_middle()
	print(rubix.colors)

	running = True
	key_to_function = {pygame.K_EQUALS : (lambda x : x.scaleAll(1.25)),
					   pygame.K_MINUS : (lambda x : x.scaleAll(0.8)),
					   pygame.K_q : (lambda x : x.rotateAll('X', 0.1)),
					   pygame.K_w : (lambda x : x.rotateAll('X', -0.1)),
					   pygame.K_a : (lambda x : x.rotateAll('Y', 0.1)),
					   pygame.K_s : (lambda x : x.rotateAll('Y', -0.1)),
					   pygame.K_z : (lambda x : x.rotateAll('Z', 0.1)),
					   pygame.K_x : (lambda x : x.rotateAll('Z', -0.1)),}

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
