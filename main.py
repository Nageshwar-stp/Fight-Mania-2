import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight Mania 2")

pygame.mixer.music.load(os.path.join('Assets', 'background.wav'))
pygame.mixer.music.play(-1, 0.0)



WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gun.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit.wav'))

HEALTH_FONT = pygame.font.SysFont('Ubuntu Mono', 20)
WINNER_FONT = pygame.font.SysFont('Ubuntu Mono', 50)


FPS = 60
VEL = 5
SPECIAL_VEL = 2
BULLET_VEL = 30
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 55

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','plane_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','plane_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space3.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
	# WIN.fill(WHITE)
	pygame.draw.rect(WIN, WHITE, BORDER)

	red_health_text = HEALTH_FONT.render("Health: "+str(red_health), 1, WHITE)
	yellow_health_text = HEALTH_FONT.render("Health: "+str(yellow_health), 1, WHITE)

	WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
	WIN.blit(yellow_health_text, (10, 10))


	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
	WIN.blit(RED_SPACESHIP, (red.x, red.y))



	for bullet in red_bullets:
		pygame.draw.rect(WIN, RED, bullet)

	for bullet in yellow_bullets:
		pygame.draw.rect(WIN, YELLOW, bullet)

	pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
	if keys_pressed == 'left' and yellow.x - SPECIAL_VEL > 0: #LEFT
			yellow.x -= SPECIAL_VEL
	if keys_pressed == 'right' and yellow.x + SPECIAL_VEL + yellow.width < BORDER.x: #RIGHT
		yellow.x += SPECIAL_VEL 
	if keys_pressed == 'up' and yellow.y - SPECIAL_VEL > 0: #UP
		yellow.y -= SPECIAL_VEL
	if keys_pressed == 'down' and yellow.y + SPECIAL_VEL + yellow.height < HEIGHT - 15: #DOWN
		yellow.y += SPECIAL_VEL

def red_handle_movement(keys_pressed, red):
	if keys_pressed[pygame.K_a] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
		red.x -= VEL
	if keys_pressed[pygame.K_d] and red.x + VEL + red.width < WIDTH: #RIGHT
		red.x += VEL 
	if keys_pressed[pygame.K_w] and red.y - VEL > 0: #UP
		red.y -= VEL
	if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT - 15: #DOWN
		red.y += VEL 


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL
		bullet.y += 1
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		elif bullet.x > WIDTH:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= BULLET_VEL
		bullet.y += 1
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)


def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))

	pygame.display.update()
	pygame.time.delay(5000)


def main():
	random_y = random.randint(100, 500)
	red = pygame.Rect(700, random_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
	yellow = pygame.Rect(100, random_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

	BACKGROUND_X = 0
	BACKGROUND_Y = 0

	red_bullets = []
	yellow_bullets = []

	red_health = 10
	yellow_health = 50

	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)

		bg_rel_y = BACKGROUND_Y%SPACE.get_rect().height

		WIN.blit(SPACE, (BACKGROUND_X,bg_rel_y))
		BACKGROUND_Y += 4

		if bg_rel_y < 600:
			WIN.blit(SPACE, (0,bg_rel_y-SPACE.get_rect().height))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				# if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
				# 	bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
				# 	yellow_bullets.append(bullet)
				# 	BULLET_FIRE_SOUND.play()

				if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
					red_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()


			if event.type == RED_HIT:
				red_health -=1
				BULLET_HIT_SOUND.play()


			if event.type == YELLOW_HIT:
				yellow_health -= 1
				BULLET_HIT_SOUND.play()


		winner_text = ""
		if red_health <= 0:
			winner_text = "Yellow Wins!"

		if yellow_health <= 0:
			winner_text = "Red Wins!"


		if winner_text != "":
			draw_winner(winner_text)
			break

		print("Red",red.x,red.y)
		print("Yellow",yellow.x, yellow.y)

		keys_pressed = pygame.key.get_pressed()		


		direction_lists = ['left','right']

		if yellow.y < red.y:
			yellow_handle_movement('down', yellow)
		elif yellow.y > red.y:
			yellow_handle_movement('up', yellow)
		elif yellow.y == red.y and len(yellow_bullets) < MAX_BULLETS:
			bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
			yellow_bullets.append(bullet)
			BULLET_FIRE_SOUND.play()
			for i in range(10):
				yellow_handle_movement('up', yellow)
			
		for i in range(20):
			yellow_handle_movement(random.choice(direction_lists), yellow)
			# pass

		
		if yellow_health <= 10 and len(yellow_bullets) < 2:
			bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
			yellow_bullets.append(bullet)
			BULLET_FIRE_SOUND.play()




		red_handle_movement(keys_pressed, red)

		handle_bullets(yellow_bullets, red_bullets, yellow, red)
		
		draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

	main()



if __name__ == "__main__":
	main()


