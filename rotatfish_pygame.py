import pygame

if __name__ == '__main__':
	# initial pygame
	pygame.init()
	# named the window
	pygame.display.set_caption("moving fish")
	# set the size of window and get the class of stage(you can say that 'screen' as background)
	screen = pygame.display.set_mode([1280,720])
	# get the class clock, it used to get the time dash between last frame and this frame
	clock = pygame.time.Clock()
	# load the image. convert can speed up the program(not sure)
	image = pygame.image.load(".\\testdata\\zebrafish.png")
	# full with black
	screen.fill([0,0,0])

	velocity = 20.
	x = 0
	y = 200

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		time_pass = clock.tick(120)
		x += time_pass*velocity/1000
		new = pygame.transform.rotate(image, x)
		screen.fill([0,0,0])
		screen.blit(image, (200,y))
		screen.blit(new, (200,y))
		pygame.display.update()
	pygame.quit()   
