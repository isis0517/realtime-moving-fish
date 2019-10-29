import pygame

if __name__ == '__main__':
	pygame.init()
	pygame.display.set_caption("OpenCV camera stream on Pygame")
	screen = pygame.display.set_mode([1280,720])
	image = pygame.image.load(".\\testdata\\zebrafish.png")
	screen.fill([0,0,0])
	screen.blit(image, (0,0))
	pygame.display.update()

	#關閉程式的程式碼
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		new = pygame.transform.rotate(image, 100)
		screen.fill([0,0,0])
		screen.blit(new, (200,200))
		pygame.display.update()
	pygame.quit()   
