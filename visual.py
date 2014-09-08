#!/usr/bin/python

import pygame
from pygame.locals import *
import math

def visualise(array):
	FPS=30
	zegar=pygame.time.Clock()
	bgcolor=(255,255,255)
	textcolor=(0,0,0)
	def load_image(name, colorkey=None):
		try:
			image = pygame.image.load(name)
		except pygame.error, message:
			print 'Couldnt load', name
			raise SystemExit, message
		image = image.convert()
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey, RLEACCEL)
		return image

	pygame.init()
	pygame.font.init()
	window = pygame.display.set_mode((1024,768))
	screen = pygame.display.get_surface()
	pygame.display.set_caption('Team Strategies Project Visualisation')
	bike=load_image("resources/moof-3.png",bgcolor)
	font = pygame.font.Font('resources/FreeMono.ttf',18)
	running = 1
	angle=0
	roll_left=1
	
	arrayIndex=0
	frameDuration=15
	frameCounter=1
	while running: 
		#fps delimiter
		zegar.tick(FPS)
		#window close
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			running = 0
		#background
		screen.fill(bgcolor)
		angle_deg = array[arrayIndex]*180/math.pi;
		rotated_bike = pygame.transform.rotate(bike,angle_deg)
		frameCounter = (frameCounter + 1) % frameDuration
		if frameCounter == 0:
			arrayIndex = arrayIndex+1
		if arrayIndex == len(array):
			running=0
		angle_display = font.render("Angle: "+str(angle_deg),0,textcolor)
		screen.blit(angle_display,(0,0))
		#display bike
		screen.blit(rotated_bike,(300,0))
		#update screen
		pygame.display.flip()
