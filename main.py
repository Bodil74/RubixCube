from WireFrame import WireFrame
from Projection import ProjectionViewer
import numpy as np
import random
import pygame
import time

pygame.init()


class Rubix:
	def __init__(self):
		self.wireframe = WireFrame()
		self.previous_moves = []
		self.moves = [((33, 30, 27, 36, 37, 38, 18, 21, 24, 47, 46, 45), True, 0),
					  ((34, 31, 28, 39, 40, 41, 19, 22, 25, 50, 49, 48), False, -1),
					  ((35, 32, 29, 42, 43, 44, 20, 23, 26, 53, 52, 51), True, 9),
					  ((2, 5, 8, 47, 50, 53, 17, 14, 11, 44, 41, 38), False, 18),
					  ((1, 4, 7, 46, 49, 52, 16, 13, 10, 43, 40, 37), False, -1),
					  ((0, 3, 6, 45, 48, 51, 15, 12, 9, 42, 39, 36), False, 27),
					  ((2, 1, 0, 27, 28, 29, 9, 10, 11, 20, 19, 18), False, 36),
					  ((5, 4, 3, 30, 31, 32, 12, 13, 14, 27, 22, 21), False, -1),
					  ((8, 7, 6, 33, 34, 35, 15, 16, 17, 26, 25, 24), False, 45)]

	def make_rubix(self):
		rubix_nodes = [(x, y, z) for x in (210, 266, 333, 400) for y in (210, 266, 333, 400) for z in (210, 266, 333, 400)]
		self.wireframe.addNodes(np.array(rubix_nodes))

		self.wireframe.addFaces([[n, n + 16, n + 20, n + 4] for n in (0, 4, 8, 16, 20, 24, 32, 36, 40, 3, 7, 11, 19, 23, 27, 35, 39, 43)])
		self.wireframe.addFaces([[n, n + 16, n + 17, n + 1] for n in (12, 13, 14, 28, 29, 30, 44, 45, 46, 0, 1, 2, 16, 17, 18, 32, 33, 34)])
		self.wireframe.addFaces([[n, n + 1, n + 5, n + 4] for n in (0, 4, 8, 1, 5, 9, 2, 6, 10, 48, 52, 56, 49, 53, 57, 50, 54, 58)])

		self.wireframe.addColors([(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0),
								  (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0), (255, 165, 0),
								  (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), 
								  (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0),
								  (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255),
								  (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0)] )

	def solve(self):
		pass	

	def undo(self):
		if len(self.previous_moves) > 0:
			call = self.previous_moves[-1]
			self.rotate(call[0], call[1], call[2])
			self.previous_moves = self.previous_moves[:-2]

	def scramble(self):
		for i in range(random.randint(100, 500)):
			r = random.randint(0, len(self.moves) - 1)
			self.rotate(self.moves[r][0], self.moves[r][1], self.moves[r][2])
			draw()

	def reset(self):
		for i in range(len(self.previous_moves[::])):
			self.undo()
			draw()

	def _rotate_side(self, side, reverse, color_copy):
		cells = [i for i in range(side, side + 9)]
		twod_cells = [[cells[n], cells[n + 1], cells[n + 2]] for n in (0, 3, 6)]
		rotated_cells = list(zip(*reversed(twod_cells)))

		if reverse:
			x = twod_cells
			twod_cells = rotated_cells
			rotated_cells = x

		for i in range(len(twod_cells)):
			for j, k in enumerate(twod_cells[i]):
				self.wireframe.colors[k] = color_copy[rotated_cells[i][j]] 

	def rotate(self, cells, reverse, side):
		self.previous_moves.append((cells, not reverse, side))
		color_copy = self.wireframe.colors.copy()
		shifted_cells = list(cells)

		for i in range(3):
			shifted_cells.insert(0, shifted_cells.pop(-1))

		if reverse:
			x = shifted_cells
			shifted_cells = cells
			cells = x

		for i, j in enumerate(shifted_cells):
			self.wireframe.colors[j] = color_copy[cells[i]]

		if side > -1:
			self._rotate_side(side, reverse, color_copy)


class MenuButtons:
	def __init__(self):
		self.font = pygame.font.SysFont('arial', 30)

		self.help_text = self.font.render('Help', True, (255, 255, 255))
		self.help_rect = pygame.Rect(535, 120, 50, 35)

		self.scramble_text = self.font.render('Scramble', True, (255, 255, 255))
		self.scramble_rect = pygame.Rect(490, 10, 105, 35)

		self.undo_text = self.font.render('Undo', True, (255, 255, 255))
		self.undo_rect = pygame.Rect(530, 80, 50, 35)

		self.reset_text = self.font.render('Reset', True, (255, 255, 255))
		self.reset_rect = pygame.Rect(525, 45, 50, 35)

	def draw(self):
		pv.screen.blit(self.help_text, (self.help_rect[0], self.help_rect[1]))
		pv.screen.blit(self.scramble_text, (self.scramble_rect[0], self.scramble_rect[1]))
		pv.screen.blit(self.undo_text, (self.undo_rect[0], self.undo_rect[1]))
		pv.screen.blit(self.reset_text, (self.reset_rect[0], self.reset_rect[1]))

	def help(self):
		opened = True
		help_rect = pygame.Rect(100, 50, 400, 500)
		help_text = pygame.image.load('./images/help_menu.png')

		while opened:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					opened = False
					pygame.quit()
					exit()

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if not pygame.Rect.collidepoint(help_rect, pygame.mouse.get_pos()):
						opened = False

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_h:
						opened = False

			pygame.draw.rect(pv.screen, (48, 48, 48), help_rect)
			pv.screen.blit(help_text, (100, 100))
			pygame.draw.rect(pv.screen, (255, 255, 255), help_rect, 1)

			pygame.display.flip()


class Timer():
	def __init__(self):
		self.start = time.time()
		self.time = time.time() - self.start
		self.font = pygame.font.SysFont('arial', 45)
		self.active = False

	def activate_deactivate(self):
		self.active = not self.active

	def draw(self):
		if self.active:
			self.time += time.time() - self.start

		self.start = time.time()
		self.text = self.font.render(f'{round(self.time, 3)}', True, (255, 255, 255))
		pv.screen.blit(self.text, (260, 500))


def draw():
	pv.display()
	menu.draw()
	timer.draw()

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
					   pygame.K_1 : (lambda x : rubix.rotate(rubix.moves[0][0], rubix.moves[0][1], rubix.moves[0][2])),
					   pygame.K_2 : (lambda x : rubix.rotate(rubix.moves[1][0], rubix.moves[1][1], rubix.moves[1][2])),
					   pygame.K_3 : (lambda x : rubix.rotate(rubix.moves[2][0], rubix.moves[2][1], rubix.moves[2][2])),
					   pygame.K_4 : (lambda x : rubix.rotate(rubix.moves[3][0], rubix.moves[3][1], rubix.moves[3][2])),
					   pygame.K_5 : (lambda x : rubix.rotate(rubix.moves[4][0], rubix.moves[4][1], rubix.moves[4][2])),
					   pygame.K_6 : (lambda x : rubix.rotate(rubix.moves[5][0], rubix.moves[5][1], rubix.moves[5][2])),
					   pygame.K_7 : (lambda x : rubix.rotate(rubix.moves[6][0], rubix.moves[6][1], rubix.moves[6][2])),
					   pygame.K_8 : (lambda x : rubix.rotate(rubix.moves[7][0], rubix.moves[7][1], rubix.moves[7][2])),
					   pygame.K_9 : (lambda x : rubix.rotate(rubix.moves[8][0], rubix.moves[8][1], rubix.moves[8][2])),
					   pygame.K_BACKSPACE : (lambda x : rubix.undo()),
					   pygame.K_u : (lambda x : rubix.scramble()),
					   pygame.K_h : (lambda x : menu.help()),
					   pygame.K_SPACE : (lambda x : timer.activate_deactivate()),
					   pygame.K_r : (lambda x : rubix.reset())}


	while running:

		draw()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			elif event.type == pygame.KEYDOWN:
				if pv.current_wireframe != False:
					if event.key in key_to_function:
						key_to_function[event.key](pv)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.Rect.collidepoint(menu.help_rect, pygame.mouse.get_pos()):
					menu.help()

				elif pygame.Rect.collidepoint(menu.scramble_rect, pygame.mouse.get_pos()):
					rubix.scramble()

				elif pygame.Rect.collidepoint(menu.undo_rect, pygame.mouse.get_pos()):
					rubix.undo()

				elif pygame.Rect.collidepoint(menu.reset_rect, pygame.mouse.get_pos()):
					rubix.reset()


menu = MenuButtons()
timer = Timer()
rubix = Rubix()
rubix.make_rubix()
pv = ProjectionViewer(600, 600, 'Rubix\'s Cube')
pv.addWireFrame('rubix', rubix.wireframe)
main()
