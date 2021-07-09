import pygame
import random

pygame.init()

win = pygame.display.set_mode((900, 750))

pygame.display.set_caption('Space Invaders by mhinzz')

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)


class Ship(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([50, 25])
		self.image.fill(green)
		self.rect = self.image.get_rect()
		self.live = 5
	def draw(self):
		win.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([25, 25])
		self.image.fill(white)
		self.rect = self.image.get_rect()
		self.groupRect = pygame.Rect(130, 75, 500, 250)
		self.direction = 5
	def update(self):
		self.rect.x += self.direction
<<<<<<< HEAD
		self.groupRect.x += self.direction
		if ((self.groupRect.x + 500) >= 875):
=======
		self.groupRect += self.direction
		if ((self.groupRect.x + 500) >= 725):
>>>>>>> parent of 32f518e (Update SpaceInvaders.py)
			self.direction = -self.direction
		if self.groupRect.x <= 25:
			self.direction = -self.direction
			self.rect.y += 5


class Bunker(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([8, 8])
		self.image.fill(green)
		self.rect = self.image.get_rect()


class Missile(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([5, 10])
		self.image.fill(green)
		self.rect = self.image.get_rect()
	def update(self):
		self.rect.y -= 10


class Bomb(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([5, 10])
		self.image.fill(red)
		self.rect = self.image.get_rect()
	def update(self):
		self.rect.y += 10


ship = Ship()
ship.rect.x = 350
ship.rect.y = 650

enemyList = pygame.sprite.Group()
bunkerList = pygame.sprite.Group()
missileList = pygame.sprite.Group()
bombList = pygame.sprite.Group()


for row in range(1, 6):
	for col in range(1, 11):
		enemy = Enemy()
		enemy.rect.x = 80 + (50 * col)
		enemy.rect.y = 25 + (50 * row)
		enemyList.add(enemy)


for bunk in range(4):
	for row in range(7):
		for col in range(15):
			bunker = Bunker()
			bunker.rect.x = (60 + ((150 + 60) * bunk)) + (10 * col)
			bunker.rect.y = 500 + (10 * row)
			bunkerList.add(bunker)


def redraw():
	win.fill(black)
	ship.draw()

	enemyList.draw(win)
	bunkerList.update()

	bunkerList.draw(win)
	missileList.update()
	missileList.draw(win)

	bombList.update()
	bombList.draw(win)

	pygame.display.update()


run = True
while run:
	pygame.time.delay(100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		ship.rect.x -= 10
	elif key[pygame.K_RIGHT]:
		ship.rect.x += 10
	if key[pygame.K_SPACE]:
		if len(missileList) < 10:
			missile = Missile()
			missile.rect.x = ship.rect.x + 25
			missile.rect.y = ship.rect.y
			missileList.add(missile)

	shootChance = random.randint(1, 100)
	if shootChance < 5:
		if len(enemyList) > 0:
			randomEnemy = random.choice(enemyList.sprites())
			bomb = Bomb()
			bomb.rect.x = randomEnemy.rect.x + 12
			bomb.rect.y = randomEnemy.rect.y + 25
			bombList.add(bomb)

	for missile in missileList:
		if missile.rect.y < -10:
			missileList.remove(missile)
		for enemy in enemyList:
			if missile.rect.colliderect(enemy.rect):
				missileList.remove(missile)
				enemyList.remove(enemy)
		for bunker in bunkerList:
			if missile.rect.colliderect(bunker.rect):
				missileList.remove(missile)
				bunkerList.remove(bunker)

	for bomb in bombList:
		if bomb.rect.y > 750:
			bombList.remove(bomb)
		for enemy in enemyList:
			if bomb.rect.colliderect(ship.rect):
				bombList.remove(bomb)
				ship.live -= 1
		for bunker in bunkerList:
			if bomb.rect.colliderect(bunker.rect):
				bombList.remove(bomb)
				bunkerList.remove(bunker)

	redraw()


pygame.quit