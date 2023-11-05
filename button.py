class call_to_action():
    def __init__(self, image, pos, text, font, base_colour, hovering_colour): # Initialize the button with given image, position, text, font, base color, and hovering color
        self.image = image         # Set the image for the button
        self.x = pos[0]         # Set the x-coordinate for the button
        self.y = pos[1]         # Set the y-coordinate for the button
        self.font = font         # Set the font for the text on the button
        self.base_colour, self.hovering_colour = base_colour, hovering_colour         # Set the base color and hovering color for the button
        self.text = text         # Set the text to be displayed on the button
        self.text_full = self.font.render(self.text, True, self.base_colour)         # Render the full text with the given font and base color

        # Initialize the rectangles for the call to action button
        if self.image is None:
            # Set the image as the text if no image is provided
            self.image = self.text_full
        # Get the rectangle for the image and center it based on x and y positions
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # Get the rectangle for the text and center it based on x and y positions
        self.text_rect = self.text_full.get_rect(center=(self.x, self.y)) #changed from self.text to self.text_full

    def update(self, screen):
        """
        Updates the call-to-action on the screen by blitting the image and text.
        """
        # Blit the image onto the screen if it exists
        if self.image is not None:
            screen.blit(self.image, self.rect)

        # Blit the text onto the screen
        screen.blit(self.text_full, self.text_rect)

    def verifyInput(self, position):
        # Check if the mouse position is within the range of the button's rectangle
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            # If yes, return True
            return True
        # If not, return False
        return False

    # This method changes the color of the button text depending on the mouse position
    def colour(self, position):
        # Check if the mouse position is within the range of the button's rectangle
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            # If yes, change the text color to the hovering color
            self.text = self.font.render(self.text, True, self.hovering_colour)
        else:
            # If not, change the text color back to the base color
            self.text = self.font.render(self.text, True, self.base_colour)


