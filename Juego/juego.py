import sys, pygame, config, random, time
import player, enemy, board, bomb, highscore, music
from pygame.locals import *
import os,sys
import threading, time
sys.path.append(os.path.split(sys.path[0])[0])
from aestrella import *
from Net import *
from mapas import *    
class Game:
	players = []
	enemies = []
	bombs = []
	resetTiles = []
	stage = 1
	level = 0
	firstRun = True
	exitGame = False
	puntosj1=0
	puntosj2=0

	def __init__(self, mode):
		self.c = config.Config()
		self.highscores = highscore.Highscore()
		self.forceQuit = False
		self.mode = mode

		pygame.init()
		self.screen = pygame.display.set_mode((self.c.WIDTH,self.c.HEIGHT),pygame.DOUBLEBUF)
		pygame.display.set_caption("Bomberman")
		
		
		# repeat for multiple levels
		while not self.exitGame: 
			self.resetGame()
			self.clearBackground()
			self.initGame()

		# launch highscores
		if not self.forceQuit:
			self.highscores.reloadScoreData()
			self.highscores.displayScore()

	def resetGame(self):
		self.field = None
		self.enemies = []
		self.bombs = []
		self.resetTiles = []

	def clearBackground(self):
		bg = pygame.Surface(self.screen.get_size())
		bg = bg.convert()
		bg.fill((0,0,0))
		self.blit(bg,(0,0))
		
        

	def initGame(self):
		if self.mode == self.c.SINGLE:
		#self.printText("Level %d-%d" % (self.stage,self.level),(40,15))
			self.field = board.Board(self.stage, self.level)
			#self.field = nmapa			
			self.timer = 0
		#elif self.mode == self.c.MULTI:
		#	self.printText("Multiplayer",(40,15))
		#	self.field = board.Board(0,0)
		#	self.timer = 5*60+1

		self.drawBoard()
		#self.drawInterface()
		self.updateTimer()

		# players do not have to be reinitialized in single player after the first time
		if self.firstRun:
			self.firstRun = False
			self.initPlayers()
		else:
			self.resetPlayerPosition(self.user,False)
		
		# no enemies in multiplayer
		if self.mode == self.c.SINGLE:
			self.initEnemies()
		
		# music player
		mp = music.Music()
		mp.playMusic(self.mode)
                self.runGame()
	# draws the board onto the screen
	def drawBoard(self):
		for row in range(1,len(self.field.board)-1):
			for col in range(1,len(self.field.board[row])-1):
				image = self.field.board[row][col].image
				# RFCT - fix the mess \/
				position = self.field.board[row][col].image.get_rect().move((col*self.c.TILE_SIZE,row*self.c.TILE_SIZE))
				self.blit(image, position)

	#def updateDisplayInfo(self):
	#	self.printText(self.user.score,(65,653))
	#	self.printText(self.user.lives,(775,653))
	#	self.printText(self.user.maxBombs,(630,653))
	#	self.printText(self.user.power,(700,653))

	#def drawInterface(self):
	#	player  = pygame.image.load(self.c.IMAGE_PATH + "screen/player.png").convert()
	#	life = pygame.image.load(self.c.IMAGE_PATH + "screen/life.png").convert()
	#	bomb = pygame.image.load(self.c.IMAGE_PATH + "screen/bomb.png").convert()
	#	power = pygame.image.load(self.c.IMAGE_PATH + "screen/power.png").convert()
	#	clock = pygame.image.load(self.c.IMAGE_PATH + "screen/clock.png").convert()

	#	self.blit(player,(40,650))
	#	self.blit(clock,(365,650))

	#	self.blit(bomb,(590,647))
	#	self.blit(power,(670,650))
	#	self.blit(life,(740,652))
	
	def initPlayers(self):
		if self.mode == self.c.SINGLE:
			self.user = player.Player("Player 1","p_1_",0,(40,40))
			self.players.append(self.user)
			self.blit(self.user.image, self.user.position)
		
                        self.user1 = player.Player("Player 2","p_2_",0,(760,40))
			self.players.append(self.user1)
			self.blit(self.user1.image, self.user1.position)
			
		
		elif self.mode == self.c.MULTI:
			for p in self.players:
				if str(p.id) == str(self.id):
					self.user = p
				self.blit(p.image,p.position)

	def initEnemies(self):
		# generates 5 enemies
		for i in range(0,5):
			while True:
				x = random.randint(6,self.field.width-2)*40			# randint(1,X) changed to 6 so enemies do not start near player
				y = random.randint(6,self.field.height-2)*40

				if self.field.getTile((x,y)).canPass() == True:
					break

			e = enemy.Enemy("Enemy", "e_%d_" % (random.randint(1,self.c.MAX_ENEMY_SPRITES)), (x,y))
			self.enemies.append(e)
			self.blit(e.image, e.position)

	def runGame(self):
		clock = pygame.time.Clock()
		pygame.time.set_timer(pygame.USEREVENT,1000)
		pygame.time.set_timer(pygame.USEREVENT+1,500)
		cyclicCounter = 0
		lacompu = 0
		pos=0
		#ruta=['s','s','a','a','a','a','a','a','a','s','s','d','d','s','s','a','a']
		astar1=AEstrella()
		if self.level==0:
                    ruta=astar1.astar(nmap, (1,1), (1,19))
		if self.level==1:
                    ruta=astar1.astar(nmapa1, (1,1), (1,19))
                if self.level==2:
                    ruta=astar1.astar(nmapa2, (1,1), (1,19))
                if self.level==3:
                    ruta=astar1.astar(nmapa3, (1,1), (1,19))
                if self.level==4:
                    ruta=astar1.astar(nmapa4, (1,1), (1,19))
                if self.level==5:
                    ruta=astar1.astar(nmapa5, (1,1), (1,19))
		self.gameIsActive = True
                
		while self.gameIsActive:
                       
			clock.tick(self.c.FPS)
			
			fin=self.checkPlayerEnemyCollision()
			#self.checkWinConditions()
                        if fin==1:
                            pos=0
			# MULTIPLAYER
			if self.mode == self.c.MULTI:
				self.tcpUpdate()
				self.manipulateTcpData()

			# self.c.FPS is set to 30, 30 ticks = 1 second
			cyclicCounter += 1
                        lacompu += 1
                        if lacompu == 7:
                                lacompu = 0
                                self.moverPC(pos,ruta)
                                pos += 1
                                if pos == len(ruta):
                                    pos=0
                                    
			if cyclicCounter == self.c.FPS:
				cyclicCounter = 0
				self.updateTimer()


			if cyclicCounter%5 == 1:
				self.clearExplosion()
				
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.forceQuit()
				elif event.type == pygame.KEYDOWN:
					# deploy bomb
					k = event.key

					if k == pygame.K_SPACE:
						if self.mode == self.c.MULTI:
							self.sendingData = ["update","bomb",k,self.id]
						self.deployBomb(self.user)
					elif k == pygame.K_ESCAPE:
						self.fQuit()
					elif k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT:
						point = self.user.movement(k) # next point
						self.movementHelper(self.user, point)
                                        elif k == pygame.K_w or k == pygame.K_s or k == pygame.K_a or k == pygame.K_d:
                                                if k==pygame.K_s:
                                                    k=pygame.K_DOWN
                                                if k==pygame.K_a:
                                                    k=pygame.K_LEFT
                                                if k==pygame.K_d:
                                                    k=pygame.K_RIGHT
                                                if k==pygame.K_w:
                                                    k=pygame.K_UP
                                                point1 = self.user1.movement(k) # next point
						self.movementHelper(self.user1, point1)
                                                
                                                
					elif k == pygame.K_g: # god mode, cheat ;)
						self.user.gainPower(self.c.BOMB_UP)
						self.user.gainPower(self.c.POWER_UP)

				elif event.type == pygame.USEREVENT: # RFCT - change definition
					self.updateBombs()
				elif event.type == pygame.USEREVENT+1: #RFCT
					for e in self.enemies:
						self.movementHelper(e,e.nextMove())

				#self.updateDisplayInfo()
				pygame.display.update()
	
	def deployBomb(self,player):
		b = player.deployBomb() # returns a bomb if available
		if b != None:
			tile = self.field.getTile(player.position)
			tile.bomb = b
			self.bombs.append(b)
		
	def blit(self,obj,pos):
		self.screen.blit(obj,pos)
	#	pygame.display.flip()
	
	def movementHelper(self, char, point):
		nPoint = char.position.move(point)
                #print nPoint
		tile = self.field.getTile(nPoint)

		# also check for bomb / special power ups here
		if tile.canPass():
			if char.instance_of == 'player' and tile.isPowerUp():
				char.setScore(50) # RFCT | BUG - VARIES DEPENDING ON POWER UP
				char.gainPower(tile.type)
				tile.destroy()
				self.blit(tile.getBackground(),nPoint)
			char.move(point)
			
			self.blit(char.image, char.position)

			t = self.field.getTile(char.old)
			if t.bomb != None:
				self.blit(t.getBackground(),char.old)
			self.blit(t.getImage(), char.old)

	def updateBombs(self):
		for bomb in self.bombs:
			if bomb.tick() == 0:
				self.activateBomb(bomb)
	
	def activateBomb(self,bomb):
		if not bomb.triggered:
			bomb.explode()
			#self.triggerBombChain(bomb)
			self.bombs.remove(bomb)
			tile = self.field.getTile(bomb.position)
			tile.bomb = None
			self.blit(tile.getImage(), bomb.position)
			self.resetTiles.append(bomb.position)

			explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_c.png").convert()
			self.blit(explosion,bomb.position)

        def explotar(self,bomb):
		if not bomb.triggered:
			bomb.explode()
			self.triggerBombChain(bomb)
			self.bombs.remove(bomb)
			tile = self.field.getTile(bomb.position)
			tile.bomb = None
			self.blit(tile.getImage(), bomb.position)
			self.resetTiles.append(bomb.position)

			explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_c.png").convert()
			self.blit(explosion,bomb.position)

	def triggerBombChain(self, bomb):
		if bomb == None:
			return
		else:
			bomb.triggered = True	
			self.bombHelper(bomb,'left')	
			self.bombHelper(bomb,'right')
			self.bombHelper(bomb,'up')
			self.bombHelper(bomb,'down')
	
	# ALGO NEEDS RFCT!!!
	def bombHelper(self, bomb, direction):
		if direction == 'right':
			point = (40,0)
		elif direction == 'left':
			point = (-40,0)
		elif direction == 'up':
			point = (0,-40)
		elif direction == 'down':
			point = (0,40)

		x = y = 0
		while True:
			x += point[0]
			y += point[1]

			nPoint = bomb.position.move((x,y))
			t = self.field.getTile(nPoint)

			# hit a block or indestructible object
			if not t.canBombPass():
				# trigger new bomb explosion
				if t.bomb != None:
					self.activateBomb(t.bomb)
				elif t.destroyable == True:
					# if brick or powerup or player
					t.destroy()
					self.blit(t.getImage(),nPoint)
					self.user.setScore(10)
				break
			else:
				# path which explosion can travel on
				self.checkPlayerEnemyBombCollision(nPoint)

				explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_c.png").convert()
				self.blit(explosion,nPoint)
				self.resetTiles.append(nPoint)
			
			# check bomb's power, this terminates the recursive loop
			if int(abs(x)/40) == bomb.range or int(abs(y)/40) == bomb.range:
				#	print "(x,y) => (" + str(x) + "," + str(y) + ")"
				break
	
	def clearExplosion(self):
		for point in self.resetTiles:
			t = self.field.getTile(point)
			self.blit(t.getImage(),point)
			self.resetTiles.remove(point)

	def resetPlayerPosition(self, player, death):
		player.reset(death)
		self.blit(player.image,player.position)
		
	def checkPlayerEnemyBombCollision(self, position):
		# check if player was hit by bomb
		for player in self.players:
			if player.position == position:
				if player.loseLifeAndGameOver():
					self.gameover(player)
				else:
					# if the player gets hit by a blast, reset it's position to the starting position
					self.resetPlayerPosition(player,True)
		
		# check if enemy was hit by bomb
		for enemy in self.enemies:
			if enemy.position == position:
				self.enemies.remove(enemy)
				self.user.setScore(100)

	def checkPlayerEnemyCollision(self):
                if self.user1.position ==(40,40,40,40):
			self.deployBomb(self.user)
			self.resetPlayerPosition(self.user1,True)
			self.resetPlayerPosition(self.user,True)
			self.victory()
			self.puntosj2 += 1
			return 1
                if self.user.position == (760,40,40,40):
                        self.deployBomb(self.user1)
                        self.resetPlayerPosition(self.user,True)
                        self.resetPlayerPosition(self.user1,True)
                        self.victory()
                        self.puntosj1 += 1
                        return 1
	#def checkWinConditions(self):
	#	if self.mode == self.c.SINGLE:
	#		if len(self.enemies) == 0:
	#			self.victory()

	def gameover(self, player):
		if self.mode == self.c.SINGLE:
			print 'gameover - lost all lives | or time ran out'
			self.highscores.addScore(player.score)
			self.gameIsActive = False
			self.exitGame = True
	
	def fQuit(self):
		self.gameIsActive = False
		self.exitGame = True
		self.forceQuit = True

	def printText(self,text,point):
	#	font = pygame.font.Font("lucida.ttf",20)
		font = pygame.font.SysFont("/home/kleber/Desktop/bomber/Juego/resources/fonts/Lucida Console",26)
		label = font.render(str(text)+'  ', True, (255,255, 255), (0, 0, 0))
		textRect = label.get_rect()
		textRect.x = point[0] 
		textRect.y = point[1]
		self.blit(label, textRect)
	
	
	
	def victory(self):
		self.gameIsActive = False
		self.user.setScore(500)
		self.level += 1
		if self.level > 5:
			self.stage += 1
			self.level = 1
		mp = music.Music()
		mp.playSound("victory")
		time.sleep(2)

	def updateTimer(self):
		self.timer += 1

		# user lost
		#if self.timer == 0:
		#	self.gameover(self.user)

		mins = str(int(self.timer/60))
		secs = str(int(self.timer%60))

		if len(mins) == 1:
			mins = "0"+mins
		if len(secs) == 1:
			secs = "0"+secs
		txt = "%s:%s" % (mins,secs)
		puntos1 = "%s:%s" % ('Harry Potter',self.puntosj1)
		puntos2 = "%s:%s" % ('Voldemor',self.puntosj2)
		self.printText(txt,(400,653))
                self.printText(puntos1,(200,653))
                self.printText(puntos2,(600,653))
		#print "mover mover :D "
		


        def moverPC(self, pos,ruta):
                k=pygame.K_DOWN
                if ruta[pos]=='D':
                    k=pygame.K_DOWN
                if ruta[pos]=='L':
                    k=pygame.K_LEFT
                if ruta[pos]=='U':
                    k=pygame.K_UP
                if ruta[pos]=='R':
                    k=pygame.K_RIGHT
                
                point1 = self.user1.movement(k) # next point
                #print point1
		self.movementHelper(self.user1, point1)
		#print self.user1.position
		


if __name__ == "__main__":
    g = Game(self.c.SINGLE)


#com  funciona hill climbing

