import pygame
import random
import math
pygame.init()

class DrawInfo:
	"""docstring for DrawInfo"""
	BLACK=0, 0,0
	WHITE=255, 255, 255
	GREEN=0, 255, 0
	RED=255, 0, 0
	BackgroundColour=WHITE

	GRAY=[
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.Font('GiddyupStd.otf', 30)
	LARGE_FONT = pygame.font.Font('GiddyupStd.otf', 40)

	SidePad=100
	TopPad=150

	def __init__(self, width, height, lst):   
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height)) 
		pygame.display.set_caption("Sorting Algorithum Visulization")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst=lst
		self.max_val = max(lst)
		self.min_val = min(lst)

		self.block_width = round((self.width - self.SidePad) / len(lst))
		self.block_height = math.floor((self.height - self.TopPad) / (self.max_val - self.min_val))
		self.start_x = self.SidePad // 2

def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BackgroundColour)
	SORT = ""
	if ascending:
		SORT = "Ascending"
	else:
		SORT = "Descending"

	title = draw_info.LARGE_FONT.render("{} - {}".format(algo_name, SORT), True, draw_info.RED)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

	controls = draw_info.FONT.render("R-Reset | Space-Start Sorting | A-Ascending | D-Descending", True, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

	sorting = draw_info.FONT.render("B-Bubble Sort | I-Insertion Sort", True, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

	draw_list(draw_info)
	pygame.display.update()

def draw_list(draw_info, color_pos={}, clear_bg=False):
	lst=draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SidePad//2, draw_info.TopPad, draw_info.width - draw_info.SidePad, draw_info.height - draw_info.TopPad)

		pygame.draw.rect(draw_info.window, draw_info.BackgroundColour, clear_rect)

	for i, val in enumerate(lst): 
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRAY[i % 3]

		if i in color_pos:
			color = color_pos[i]

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))


	if clear_bg:
		pygame.display.update()


def generate_list(n, min_val, max_val):
	lst = []

	for i in range(n):
		val=random.randint(min_val, max_val)
		lst.append(val)

	return lst

def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst)-1):
		for j in range(len(lst)-1-i):
			if(lst[j]>lst[j+1] and ascending) or (lst[j]<lst[j+1] and not ascending):
				lst[j], lst[j+1] = lst[j+1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True) 
				yield True #imp

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst)):
		x=i
		for j in range(i, 0, -1):
			if (lst[x]<lst[j-1] and ascending) or (lst[x]>lst[j-1] and not ascending):
				lst[x], lst[j-1] = lst[j-1], lst[x]
				draw_list(draw_info, {j-1: draw_info.GREEN, x: draw_info.RED}, True)
				x=x-1
				yield True

	return lst


def main():
	run=True
	clock = pygame.time.Clock()
	n=50
	min_val=0
	max_val=100
	lst = generate_list(n, min_val, max_val)
	draw_info = DrawInfo(800, 600, lst) 
	sorting = False
	ascending = True

	sorting_algo = bubble_sort
	sorting_algo_name = "BUBBLE SORT"
	sorting_algo_generator = None

	while run:
		clock.tick(60)

		if sorting:
			try:
				next(sorting_algo_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run=False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst=generate_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False

			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algo_generator = sorting_algo(draw_info, ascending)

			elif event.key == pygame.K_a and not sorting:
				ascending = True

			elif event.key == pygame.K_d and not sorting:
				ascending = False

			elif event.key == pygame.K_b and not sorting:
				sorting_algo = bubble_sort
				sorting_algo_name = "Bubble Sort"

			elif event.key == pygame.K_i and not sorting:
				sorting_algo = insertion_sort
				sorting_algo_name = "Insertion Sort"

	pygame.quit()


if __name__=="__main__":
	main ( )
