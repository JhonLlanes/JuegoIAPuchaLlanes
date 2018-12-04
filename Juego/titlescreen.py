import sys, pygame, config, juego, highscore

class Titlescreen():

	def __init__(self):
		self.c = config.Config()
		exitMain = False

		while not exitMain:
			pygame.init()
			self.screen = pygame.display.set_mode((1028,768))
			pygame.display.set_caption("Bomberman")
			clock = pygame.time.Clock()
                        g = juego.Game(self.c.SINGLE)
			

if __name__ == "__main__":
    t = Titlescreen()
    g = juego.Game(self.c.SINGLE)
