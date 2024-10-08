import pgzrun
import pgzero.screen
screen: pgzero.screen.Screen
from pgzhelper import *
import pygame
import os
import random
import time

# Set up the game screen
WIDTH = 640
HEIGHT = 480
TITLE = 'Flappy Bird'

# Sound 
wing_sound = pygame.mixer.Sound(os.path.join('sounds', 'wing.wav'))

# Ground
ground = Actor('ground')
ground.x = 320
ground.y = 465

# Bird
bird = Actor('bird0')
bird.x = 100
bird.y = 250
bird.images = ['bird0', 'bird1', 'bird2']
bird.fps = 10

# Game Over
gameover = Actor('gameover')
gameover.x = 320
gameover.y = 200
gameover.scale = 0.3

# Message (instructions)
message = Actor('message')
message.x = 320
message.y = 240

# Pipes
top_pipe = Actor('top')
bottom_pipe = Actor('bottom')
top_pipe.x = 640
top_pipe.y = -100
gap = 125
bottom_pipe.x = 640
bottom_pipe.y = top_pipe.height + gap

# Coin
coin = Actor('coin1')
coin.x = 640
coin.y = bottom_pipe.height + 50
coin.images = ['coin1', 'coin2', 'coin3', 'coin4', 'coin5', 'coin6']
coin.fps = 10
coin_collected = False

# Set up game variables
gravity = 0.3  # How fast the bird falls towards the ground
bird.speed = 1  # How fast the bird moves up/down
bird.alive = True
scroll_speed = -4
score = 0
top_score = 0  # Variable to store the top score
mode = 'menu'
countdown = 3
start_time = None
countdown_active = False

def on_mouse_down():
    global score, mode, countdown, start_time, countdown_active

    wing_sound.play()  # make sure wing sound is played in mode menu and game
    if mode == 'menu' and not countdown_active:     
        start_time = time.time()
        countdown_active = True

    elif mode == 'game':
        if bird.alive:
            bird.speed = -6.5  # Make the bird fly up a little
        else:
            bird.alive = True  # Restart the game
            score = 0

def update():
    global gap, score, top_score, mode, countdown, start_time, countdown_active, coin_collected
    
    # Animate bird in both 'menu' and 'game' modes
    bird.animate()
    coin.animate()
    
    # Make countdown for 5 seconds before the game start
    if mode == 'menu' and countdown_active:
        elapsed_time = time.time() - start_time
        countdown = 3 - int(elapsed_time)
        if countdown <= 0:
            mode = 'game'
            countdown_active = False

    elif mode == 'game':
        bird.y = bird.y + bird.speed
        bird.speed = bird.speed + gravity
        
        if bird.y > HEIGHT - 40 or bird.y < 0:
            bird.alive = False
            sounds.die.play()
            if score > top_score:
                top_score = score  # Update top score if the current score is higher

        top_pipe.x = top_pipe.x + scroll_speed
        bottom_pipe.x = bottom_pipe.x + scroll_speed
        coin.x = coin.x + scroll_speed
            
        if top_pipe.x < -50:
            offset = random.uniform(-100, -200)
            top_pipe.midleft = (640, offset)
            bottom_pipe.midleft = (640, offset + top_pipe.height + gap)
            
            # Position the coin in the center of the gap between the pipes
            coin.midleft = (660, offset + 320)
            coin_collected = False  # Reset the coin collection status
            
            gap = random.randint(120, 150)
            score = score + 1
            sounds.point.play()

        if bird.colliderect(top_pipe) or bird.colliderect(bottom_pipe):
            bird.alive = False
            sounds.hit.play()

        # Check for collision with the coin
        if bird.colliderect(coin) and not coin_collected:
            coin_collected = True
            score += 5  # Add extra points for collecting the coin
            coin.x = -100  # Move the coin off-screen after collection

def draw():
    screen.blit('bg', (0, 0))

    if mode == 'menu':
        bird.draw()
        message.draw()
        # Display countdown 
        if countdown_active:
            screen.draw.text(f'Are You Ready {countdown}', color='white', center=(320, 50), shadow=(0.5, 0.5), scolor='black', fontsize=50)

    elif mode == 'game':    
        if bird.alive:
            top_pipe.draw()
            bottom_pipe.draw()
            if not coin_collected:  # Draw the coin only if it has not been collected
                coin.draw()
            bird.draw()        
            ground.draw()
            
        else:
            screen.draw.text('Click your mouse to play again', color='white', center=(320, 300), shadow=(0.5, 0.5), scolor='black', fontsize=30)
            gameover.draw()
            bird.x = 75
            bird.y = 100
            gravity = 0
            bird.speed = 0
            top_pipe.x = 640
            bottom_pipe.x = 640

        screen.draw.text('Score: ' + str(score), color='white', midtop=(50, 10), shadow=(0.5, 0.5), scolor='black', fontsize=30)
        screen.draw.text(f'Top Score: {top_score}', color='white', topright=(620, 10), shadow=(0.5, 0.5), scolor='black', fontsize=30)

pgzrun.go()
