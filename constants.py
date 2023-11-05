#import pygame modules to load up image
import pygame 
pygame.init()

#   colours
black  = (  0,  0,  0)
empty = (1, 1, 1) #arbitrary value to store the locations on the board which do not have a piece
white  = (255,255,255)
red    = (255,  0,  0)
yellow = (255,255,  0)
boardImg = pygame.image.load("board1.jpg") #loads the checkers board image

screen = pygame.display.Info()
WIDTH, HEIGHT = screen.current_w, screen.current_h #Set the old width and height variables to the current width and height of the screen

BACKDROP = pygame.transform.scale(pygame.image.load("backdrop.jpg"), (WIDTH,HEIGHT)) #loads the backdrop as a variable called BACKDROP
B_PIECE = [pygame.transform.scale(pygame.image.load('Coins/Coin1.png'), (200,200)), pygame.transform.scale(pygame.image.load('Coins/Coin2.png'), (200,200)), pygame.transform.scale(pygame.image.load('Coins/Coin3.png'), (200,200)),
           pygame.transform.scale(pygame.image.load('Coins/Coin4.png'), (200,200)), pygame.transform.scale(pygame.image.load('Coins/Coin5.png'), (200,200)), pygame.transform.scale(pygame.image.load('Coins/Coin6.png'), (200,200))] #png image of black checkers piece
W_PIECE = [pygame.transform.scale(pygame.image.load('WCoins/Coin1.png'), (200,200)), pygame.transform.scale(pygame.image.load('WCoins/Coin2.png'), (200,200)), pygame.transform.scale(pygame.image.load('WCoins/Coin3.png'), (200,200)),
           pygame.transform.scale(pygame.image.load('WCoins/Coin4.png'), (200,200)), pygame.transform.scale(pygame.image.load('WCoins/Coin5.png'), (200,200)), pygame.transform.scale(pygame.image.load('WCoins/Coin6.png'), (200,200))] #png image of white checkers piece
R_PIECE = [pygame.transform.scale(pygame.image.load('Coins/Coin1.png'), (200,200)), pygame.transform.scale(pygame.image.load('Coins/Coin2.png'), (200,200)), pygame.transform.scale(pygame.image.load('Coins/Coin3.png'), (200,200)),
           pygame.transform.scale(pygame.image.load('WCoins/Coin4.png'), (200,200)), pygame.transform.scale(pygame.image.load('WCoins/Coin5.png'), (200,200)), pygame.transform.scale(pygame.image.load('WCoins/Coin6.png'), (200,200))]
           
button_width = 100
button_height = 50
button_pos = (150, 175)



blue   = (  0,  0, 255) 