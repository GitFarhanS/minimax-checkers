import pygame
import sys
import random
from Tkinter import *
from menuSys.newCheckers import startMenu
from menuSys.button import call_to_action
from menuSys.checkers.constants import WIDTH, HEIGHT, BACKDROP, W_PIECE, B_PIECE, R_PIECE, button_width, button_height, button_pos
from login import Login

pygame.mixer.init() #initialises music
pygame.mixer.music.load('music.mp3') #selects the file of the music
pygame.mixer.music.play(-1)


MENU = pygame.display.set_mode((WIDTH, HEIGHT)) #Initialize the display with a window of size WIDTH and HEIGHT
pygame.display.set_caption("Menu") #Initialize the display with a window of size WIDTH and HEIGHT



def retrieve_font(size): # Returns the words in the desired size
    return pygame.font.Font("font.otf", size)

def game(): # Keep displaying the menu screen until the user exits
    last_update = pygame.time.get_ticks() #find the amound of ticks when running
    animation_cooldown = 90 #sets the amound of miliseconds before moving to next frame
    frame = 0 #this is the first sprite of my images
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos() # Get the current mouse position
        MENU.fill("black") # Fill the screen with black
        GAME_TEXT = retrieve_font(45).render("Pick BLACK, WHITE or RANDOM", True, "White") # Render the "Pick BLACK, WHITE or RANDOM" text with white color and specified font size
        GAME_RECT = GAME_TEXT.get_rect(center=(WIDTH//2, HEIGHT//4)) # Get the rectangular area of the text surface, changed from 460 to 260
        MENU.blit(GAME_TEXT, GAME_RECT) # Blit the text surface onto the menu screen at the specified position (center of the screen)

        #update image animation
        current_time = pygame.time.get_ticks() #create the current_time variable
        if current_time - last_update >= animation_cooldown: #whenever the animation cooldown is passed the sprite is images is changed
            frame +=1 #chagnes to the next frame
            last_update = current_time #changes the last update to the current time
            if frame >= len(B_PIECE): #finds when the animation his reachd the last fram then resets it
                frame = 0

        #MENU.blit(B_PIECE[frame], (WIDTH//3.4, HEIGHT//3)) # shows the animation of the black piece
        #MENU.blit(W_PIECE[frame], (WIDTH//2.2, HEIGHT // 3)) # shows the animation of the white piece
        #MENU.blit(R_PIECE[frame], (WIDTH // 1.6, HEIGHT // 3)) # shows the animation of the random piece

        PLAY_WHITE = call_to_action(image=W_PIECE[frame], pos=(WIDTH // 2, HEIGHT // 2.4), text=None,
                                    font=retrieve_font(0), base_colour="White", hovering_colour="Green")
        PLAY_BLACK = call_to_action(image=B_PIECE[frame], pos=(WIDTH//2.9, HEIGHT//2.4), text=None, font=retrieve_font(0), base_colour="White", hovering_colour="Green")
        PLAY_RANDOM= call_to_action(image=R_PIECE[frame], pos=(WIDTH // 1.5, HEIGHT // 2.4), text=None,
                                    font=retrieve_font(0), base_colour="White", hovering_colour="Green")
        #creates another rotation black pice which can be clicked to performa function
        GAME_BACK = call_to_action(image=None, pos=(WIDTH//2, HEIGHT//1.5), text="BACK", font=retrieve_font(75), base_colour="White", hovering_colour="Green")

        # Update the color of the button text based on the mouse position
        GAME_BACK.colour(PLAY_MOUSE_POS)

        # Draw the button on the screen
        GAME_BACK.update(MENU)
        PLAY_BLACK.update(MENU)
        PLAY_WHITE.update(MENU)
        PLAY_RANDOM.update(MENU)

        # Handle events
        for event in pygame.event.get():
            # If the event is to quit the game, quit pygame and exit the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If the event is a mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse position is within the range of the button's rectangle
                if GAME_BACK.verifyInput(PLAY_MOUSE_POS):
                    # If yes, call the main menu function
                    main_menu()
                if PLAY_BLACK.verifyInput(PLAY_MOUSE_POS): #runs the game as black to be the player
                    menu_instance = startMenu()
                    menu_instance.runMain(0) 
                if PLAY_WHITE.verifyInput(PLAY_MOUSE_POS): #runs the game as white to be the player
                    menu_instance = startMenu()
                    menu_instance.runMain(1)
                if PLAY_RANDOM.verifyInput(PLAY_MOUSE_POS): #runs the game as random to be the player
                    randomise = random.randint(0, 1) #creates a random option
                    menu_instance = startMenu()
                    menu_instance.runMain(randomise)

        # Update the display
        pygame.display.update()


# Function to display the settings screen
def settings():
    music_on = True #flag for music
    flag = False #flag for mous button down
    _loggedin  = False
    MUSIC = call_to_action(image=None, pos=(WIDTH//2, HEIGHT//2), text="MUSIC OFF", font=retrieve_font(75), #shows the MUSIC OF TEXT
                                                    base_colour="Black", hovering_colour="Green")
    # Infinite loop to display the settings screen until the user returns to the main menu
    while True:
        # Get the current mouse position
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()

        # Fill the display with the "white" color
        MENU.fill("white")

        # Render the text "This is the OPTIONS screen." using the font of size 45, in black color
        SETTINGS_TEXT = retrieve_font(45).render("This is the OPTIONS screen.", True, "Black")

        # Get the rectangle object that surrounds the text and set its center to (640, 260)
        SETTINGS_RECT = SETTINGS_TEXT.get_rect(center=(WIDTH//2, HEIGHT//5))

        # Blit the text onto the display
        MENU.blit(SETTINGS_TEXT, SETTINGS_RECT)

        # Create a new instance of the call_to_action class with specific parameters
        OPTIONS_BACK = call_to_action(image=None, pos=(WIDTH//2, HEIGHT//1.5), text="BACK", font=retrieve_font(75),
                                      base_colour="Black", hovering_colour="Green")
        
        LOGIN = call_to_action(image=None, pos=(WIDTH//2, HEIGHT//3), text="LOGIN", font = retrieve_font(75), #shows the LOGIN
                                                    base_colour="Black", hovering_colour="Green")

        
        if MUSIC.verifyInput(SETTINGS_MOUSE_POS) and flag:
            # If the button is clicked, toggle the music state and play or stop music accordingly
            music_on = not music_on #when clikced change the state of variable
            if music_on:
                pygame.mixer.music.play(-1) #plays the music
                MUSIC = call_to_action(image=None, pos=(WIDTH//2, HEIGHT//2), text="MUSIC OFF", font=retrieve_font(75), #displays the correct text after running
                                                    base_colour="Black", hovering_colour="Green")
                flag = False
            else:
                pygame.mixer.music.stop() #stops the music
                MUSIC = call_to_action(image=None, pos=(WIDTH//2, HEIGHT//2), text="MUSIC ON", font=retrieve_font(75), #displays the correct text after running
                                                    base_colour="Black", hovering_colour="Green")
                flag = False

        if _loggedin:
            # Render the text "This is the USER ." using the font of size 75, in black color
            USER = retrieve_font(75).render("Welcome " + user, True, "Black")

            # Render the text "This is the SCORE ." using the font of size 75, in black color
            SCORE = pygame.font.Font("font2.ttf", 75).render("You have a score of:" + str(0), True, "Black")

            # Get the rectangle object that surrounds the text and set its center to (640, 260)
            USER_RECT = USER.get_rect(center=(WIDTH//2, HEIGHT//5/6))

            # Get the rectangle object that surrounds the text and set its center to (640, 260)
            SCORE_RECT = SCORE.get_rect(center=(WIDTH//2, HEIGHT//1.1))

            # Update the button text based on the new music state

            MENU.blit(USER, USER_RECT)
            MENU.blit(SCORE, SCORE_RECT)

        # Apply the hovering color to the button based on the mouse position
        OPTIONS_BACK.colour(SETTINGS_MOUSE_POS)

        # Update the button on the screen
        OPTIONS_BACK.update(MENU)

        # Update the button on the screen
        MUSIC.update(MENU)

        # Update the button on the screen
        LOGIN.update(MENU)

        # Check for any events in the Pygame event queue
        for event in pygame.event.get():
            # If the event is a quit event, quit Pygame and exit the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If the event is a mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse position is within the button's rectangle
                if OPTIONS_BACK.verifyInput(SETTINGS_MOUSE_POS):
                    # If it is, go back to the main menu
                    main_menu()
                if MUSIC.verifyInput(SETTINGS_MOUSE_POS):
                    flag = True
                if LOGIN.verifyInput(SETTINGS_MOUSE_POS):
                    root = Tk()
                    obj = Login(root)
                    root.mainloop()

                    user = obj.loggedin #gets username
                    #score = obj.score #gets score
                    _loggedin = True


        # Update the display with the changes
        pygame.display.update()


# Define the main_menu function
def main_menu():
    # Start the infinite loop for the main menu
    while True:
        # Display the background image
        MENU.blit(BACKDROP, (0, 0))

        # Get the mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Render and display the main menu text
        MENU_TEXT = retrieve_font(100).render("MAIN)MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, HEIGHT//6)) #scales it so that it is centered horizonatally and a sixth way down from the top

        # Call to action buttons with images, text, font, base and hovering color
        # Play button
        #GAME_BUTTON = call_to_action(image=pygame.image.load("Play Rect.png"), pos=(640, 250), text="Start Game", font=retrieve_font(75), base_colour=(255,255,255), hovering_colour=(0,0,0))
        GAME_BUTTON = call_to_action(image=pygame.image.load("PlayRect.png"), pos=(WIDTH//2, HEIGHT//3), text="PLAY", font=retrieve_font(75), base_colour="#d7fcd4", hovering_colour="White") #scales it so that it is centered horizonatally and a third way down from the top

        # Options button
        SETTINGS_BUTTON = call_to_action(image=pygame.image.load("OptionsRect.png"), pos=(WIDTH//2, HEIGHT//2), #scales it so that it is centered horizonatally and a half way down from the top
                                text="OPTIONS", font=retrieve_font(75), base_colour="#d7fcd4", hovering_colour="White")
        # Quit button
        QUIT_BUTTON = call_to_action(image=pygame.image.load("QuitRect.png"), pos=(WIDTH//2, HEIGHT//1.5),#scales it so that it is centered horizonatally
                             text="QUIT", font=retrieve_font(75), base_colour="#d7fcd4", hovering_colour="White")

        # First, the code is displaying the text "MAIN MENU" in the center of the screen by first rendering it and storing it in the variable `MENU_TEXT`,
        # then calculating its rectangle (`MENU_RECT`) to center it on the screen, and finally blitting it onto the `MENU` surface.
        MENU.blit(MENU_TEXT, MENU_RECT)

        # Next, the code is updating the color of the buttons depending on if the mouse is hovering over them by using a for loop to iterate over the buttons stored in the list `[GAME_BUTTON, SETTINGS_BUTTON, QUIT_BUTTON]`.
        # For each button, the code calls the `colour()` method and passes the `MENU_MOUSE_POS` variable which contains the current mouse position.
        # The `update()` method is then called on each button to update it on the `MENU` surface.
        for button in [GAME_BUTTON, SETTINGS_BUTTON, QUIT_BUTTON]: #changed from call_to_action to button
            button.colour(MENU_MOUSE_POS)
            button.update(MENU)

        # In the event loop, the code is checking if the user has quit the game by clicking the close button or by pressing the 'X' key.
        # If the event type is `pygame.QUIT`, the game is exited using `pygame.quit()` and `sys.exit()`.
        # If the event type is `pygame.MOUSEBUTTONDOWN`, the code is checking which button the user has clicked by calling the `verifyInput()` method on each button and passing `MENU_MOUSE_POS` as an argument.
        # If the `verifyInput()` method returns `True`, the corresponding action is performed (either `game()`, `settings()`, or quitting the game).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GAME_BUTTON.verifyInput(MENU_MOUSE_POS):
                    game()
                if SETTINGS_BUTTON.verifyInput(MENU_MOUSE_POS):
                    settings()
                if QUIT_BUTTON.verifyInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # The `pygame.display.update()` method is called to update the display with any changes made to the `MENU` surface.
        pygame.display.update()

# The `main_menu()` function is called to start the main menu.
main_menu()