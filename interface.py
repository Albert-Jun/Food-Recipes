import sys
from typing import Optional

import pygame

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 700
logo_img = pygame.image.load('assets/logo.png')

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sustainable Table')
pygame.display.set_icon(logo_img)

font_path = 'assets/GROBOLD.ttf'  # Replace with the actual path to your font file
font_size = 10

# Load the custom font
custom_font = pygame.font.Font(font_path, font_size)

start_img = pygame.image.load('assets/buttons/start_btn.png').convert_alpha()
next_img = pygame.image.load('assets/buttons/next_btn.png').convert_alpha()
food_img = pygame.image.load('assets/buttons/food_btn.png').convert_alpha()
start_img_hover = pygame.image.load('assets/buttons/start_btn_hover.png').convert_alpha()
next_img_hover = pygame.image.load('assets/buttons/next_btn_hover.png').convert_alpha()
food_img_hover = pygame.image.load('assets/buttons/food_btn_hover.png').convert_alpha()
toggle_img = pygame.image.load('assets/buttons/toggle_btn.png').convert_alpha()
toggle_clicked_img = pygame.image.load('assets/buttons/toggle_btn_clicked.png').convert_alpha()
toggle_hover_img = pygame.image.load('assets/buttons/toggle_btn_hover.png').convert_alpha()
toggle_hover_clicked_img = pygame.image.load('assets/buttons/toggle_btn_clicked_hover.png').convert_alpha()
subcat_img = pygame.image.load('assets/subcat.png')
difficult_img = pygame.image.load('assets/difficult.png')
serves_img = pygame.image.load('assets/serves.png')
nutrients_img = pygame.image.load('assets/nutrients.png')
times_img = pygame.image.load('assets/times.png')
bg_img = pygame.image.load('assets/bg_img.png')

food1_img = pygame.image.load('assets/food1.jpg')
food2_img = pygame.image.load('assets/food2.jpg')
food3_img = pygame.image.load('assets/food3.jpg')
food4_img = pygame.image.load('assets/food4.jpg')
food5_img = pygame.image.load('assets/food5.jpg')


class Button:
    """Button Instance"""

    def __init__(self, name, x, y, image, image_pressed, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width) * scale, int(height) * scale))
        self.image_pressed = pygame.transform.scale(image_pressed, (int(width) * scale, int(height) * scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.name = name

    def draw(self):
        """
            Draws
        """
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouse is over and clicked ocndition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if self.rect.collidepoint(pos):
            screen.blit(self.image_pressed, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


class Toggle(Button):
    def __init__(self, name, x, y, image, image_hover, image_pressed, image_pressed_hover, scale_norm, scale_pressed):
        super().__init__(name, x, y, image, image_pressed, scale_norm)
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale_norm), int(height * scale_norm)))
        self.image_hover = pygame.transform.scale(image_hover, (int(width * scale_norm), int(height * scale_norm)))
        self.image_pressed = pygame.transform.scale(image_pressed,
                                                    (int(width * scale_pressed), int(height * scale_pressed)))
        self.image_pressed_hover = pygame.transform.scale(image_pressed_hover,
                                                          (int(width * scale_pressed), int(height * scale_pressed)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.click_pending = False  # To track if a click is in process
        self.name = name

    def draw(self):
        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(pos):
            if mouse_pressed and not self.click_pending:
                self.click_pending = True  # Mark that a click started
            elif not mouse_pressed and self.click_pending:
                # Only toggle if the mouse was clicked and then released while over the button
                self.clicked = not self.clicked
                self.click_pending = False  # Reset click tracking
                print(f'{self.name} is Toggled' if self.clicked else f'{self.name} is untoggled')

        if self.rect.collidepoint(pos):
            if self.clicked is False:
                screen.blit(self.image_hover, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image_pressed_hover, (self.rect.x, self.rect.y))

        else:
            if mouse_pressed and self.click_pending:
                self.click_pending = False  # Cancel the click if mouse moves out
            screen.blit(self.image_pressed if self.clicked else self.image, self.rect)

        return self.clicked

    def set_allowed_click(self, allow):
        self.click_pending = allow


class TextImageButton(Button):
    """Button with text, image, and star rating that changes text color on hover."""

    def __init__(self, name, x, y, image, image_pressed, scale, text, font, text_color, text_hover_color, rating,
                 left_image):
        super().__init__(name, x, y, image, image_pressed, scale)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.text_hover_color = text_hover_color
        self.rating = rating  # Integer rating from 1 to 5
        self.left_image = pygame.transform.scale(left_image, (80, 80))  # Load the image to display to the left of the text
        self.star_full = pygame.image.load('assets/buttons/stars_full.png')  # Load your full star image
        self.star_empty = pygame.image.load('assets/buttons/stars_empty.png')  # Load your empty star image

        # Initial text color
        self.current_text_color = text_color
        # Render the text
        self.text_surface = self.font.render(self.text, True, self.current_text_color)
        # Calculate text position to center it on the button, adjusting for the left image
        self.text_x = self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2
        self.text_y = self.rect.y + (
                    self.rect.height - self.text_surface.get_height() - self.star_full.get_height()) // 2

    def draw(self):
        """
        Draws the button, text, and star rating on top of it within the button bounds.
        Adjusts the text color based on mouse hover.
        """
        global screen  # Assuming 'screen' is defined globally

        action = super().draw()  # Call the draw method of the base class to draw the button

        # Draw the left image to the left of the text if needed
        left_img_x = self.text_x - self.left_image.get_width() - 30  # Adjust position as necessary
        left_img_y = self.rect.y + (self.rect.height - self.left_image.get_height()) // 2
        screen.blit(self.left_image, (left_img_x, left_img_y))

        # Check for mouse hover to determine text color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.current_text_color != self.text_hover_color:
                self.current_text_color = self.text_hover_color
                self.text_surface = self.font.render(self.text, True, self.current_text_color)
        else:
            if self.current_text_color != self.text_color:
                self.current_text_color = self.text_color
                self.text_surface = self.font.render(self.text, True, self.current_text_color)

        # Draw the text surface onto the screen at its calculated position
        screen.blit(self.text_surface, (self.text_x, self.text_y))

        # Render the star rating below the text
        stars_x_base = self.text_x + (
                    self.text_surface.get_width() - 5 * self.star_full.get_width() - 4 * 5) / 2  # Center stars relative to text
        for i in range(5):
            star_x = stars_x_base + i * (self.star_full.get_width() + 5)  # Adjust spacing as needed
            star_y = self.text_y + self.text_surface.get_height() + 5  # Position stars just below the text
            if i < self.rating:
                screen.blit(self.star_full, (star_x, star_y))
            else:
                screen.blit(self.star_empty, (star_x, star_y))

        return action


class MultipleToggle():
    def __init__(self, buttons: list):
        self.buttons = buttons
        if any([button.clicked is True for button in self.buttons]):
            self.status = True
        else:
            self.status = False
        if self.status is True:
            self.allowed_toggle = False
        else:
            self.allowed_toggle = True

    def get_status(self):
        return [button.clicked for button in self.buttons]

    def allowed_toggle(self):
        return self.allowed_toggle

    def draw(self):
        for button in self.buttons:
            button.draw()


start_button = Button('start_btn', 230, 230, start_img, start_img_hover, 1)
next_button = Button('next_btn', 400, 500, next_img, next_img_hover, 1 / 2)
next_button2 = Button('next_btn2', 400, 500, next_img, next_img_hover, 1 / 2)
food_button1 = TextImageButton('food_btn1', 50, 85, food_img, food_img_hover, 1, 'SAMPLE FOOD1',
                               custom_font, (0, 0, 0), (255, 255, 255), 1, food1_img)
food_button2 = TextImageButton('food_btn2', 50, 200, food_img, food_img_hover, 1, 'SAMPLE FOOD2',
                               custom_font, (0, 0, 0), (255, 255, 255), 2, food2_img)
food_button3 = TextImageButton('food_btn3', 50, 315, food_img, food_img_hover, 1, 'SAMPLE FOOD3',
                               custom_font, (0, 0, 0), (255, 255, 255), 3, food3_img)
food_button4 = TextImageButton('food_btn4', 50, 430, food_img, food_img_hover, 1, 'SAMPLE FOOD4',
                               custom_font, (0, 0, 0), (255, 255, 255), 4, food4_img)
food_button5 = TextImageButton('food_btn5', 50, 545, food_img, food_img_hover, 1, 'SAMPLE FOOD5',
                               custom_font, (0, 0, 0), (255, 255, 255), 5, food5_img)
toggle_button1 = Toggle('tog_btn1', 100, 500, toggle_img, toggle_hover_img, toggle_clicked_img,
                        toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button2 = Toggle('tog_btn2', 100, 200, toggle_img, toggle_hover_img, toggle_clicked_img,
                        toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button3 = Toggle('tog_btn3', 100, 300, toggle_img, toggle_hover_img, toggle_clicked_img,
                        toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button4 = Toggle('tog_btn4', 100, 400, toggle_img, toggle_hover_img, toggle_clicked_img,
                        toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button5 = Toggle('tog_btn5', 100, 400, toggle_img, toggle_hover_img, toggle_clicked_img,
                        toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button6 = Toggle('tog_btn6', 100, 200, toggle_img, toggle_hover_img, toggle_clicked_img,
                        toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button7 = Toggle('tog_btn7', 100, 300, toggle_img, toggle_hover_img, toggle_clicked_img,
                        toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button8 = Toggle('tog_btn8', 100, 500, toggle_img, toggle_hover_img, toggle_clicked_img,
                        toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button9 = Toggle('tog_btn9', 100, 400, toggle_img, toggle_hover_img, toggle_clicked_img,
                        toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button10 = Toggle('tog_btn10', 100, 200, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button11 = Toggle('tog_btn11', 100, 300, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button12 = Toggle('tog_btn12', 100, 500, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button13 = Toggle('tog_btn13', 100, 400, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button14 = Toggle('tog_btn14', 100, 200, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button15 = Toggle('tog_btn15', 100, 300, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button16 = Toggle('tog_btn16', 100, 500, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button17 = Toggle('tog_btn17', 100, 400, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button18 = Toggle('tog_btn18', 100, 200, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button19 = Toggle('tog_btn19', 100, 300, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_button20 = Toggle('tog_btn20', 100, 500, toggle_img, toggle_hover_img, toggle_clicked_img,
                         toggle_hover_clicked_img, 1 / 2, 1 / 2)
toggle_group1 = [toggle_button5, toggle_button6, toggle_button7, toggle_button8]
toggle_group2 = [toggle_button9, toggle_button10, toggle_button11, toggle_button12]
toggle_group3 = [toggle_button13, toggle_button14, toggle_button15, toggle_button16]
toggle_group4 = [toggle_button17, toggle_button18, toggle_button19, toggle_button20]


class Interface:
    def __init__(self):
        self.status = True


class MainMenu(Interface):
    def __init__(self):
        self.status = True
        self.start = False
        self.option = False

    def run(self):
        screen.blit(bg_img, (0, 0))
        # screen.fill((3, 252, 82))

        if start_button.draw():
            self.start = True


class Subcatergory(Interface):
    def __init__(self):
        self.status = True
        self.toggle = False
        self.next = False

    def run(self, buttons: list):
        screen.fill((47, 82, 54))
        screen.blit(subcat_img, (0, 0))
        group = MultipleToggle(buttons)
        group.draw()

        if not group.allowed_toggle:
            for i in range(len(group.buttons)):
                if group.get_status()[i] is False:
                    group.buttons[i].set_allowed_click(False)
            self.toggle = True
        else:
            self.toggle = False

        if self.toggle:
            if next_button2.draw():
                self.next = True


class Difficulty(Interface):
    def __init__(self):
        self.status = True
        self.toggle = False
        self.next = False

    def run(self, buttons: list):
        screen.fill((47, 82, 54))
        screen.blit(difficult_img, (0, 0))
        group = MultipleToggle(buttons)
        group.draw()

        if not group.allowed_toggle:
            for i in range(len(group.buttons)):
                if group.get_status()[i] is False:
                    group.buttons[i].set_allowed_click(False)
            self.toggle = True
        else:
            self.toggle = False

        if self.toggle:
            if next_button2.draw():
                self.next = True


class Serves(Interface):
    def __init__(self):
        self.status = True
        self.toggle = False
        self.next = False

    def run(self, buttons: list):
        screen.fill((47, 82, 54))
        screen.blit(serves_img, (0, 0))
        group = MultipleToggle(buttons)
        group.draw()

        if not group.allowed_toggle:
            for i in range(len(group.buttons)):
                if group.get_status()[i] is False:
                    group.buttons[i].set_allowed_click(False)
            self.toggle = True
        else:
            self.toggle = False

        if self.toggle:
            if next_button2.draw():
                self.next = True


class Nutrients(Interface):
    def __init__(self):
        self.status = True
        self.toggle1 = False
        self.toggle2 = False
        self.toggle3 = False
        self.toggle4 = False
        self.next = False
        self.first = True

    def run(self):
        screen.fill((47, 82, 54))
        screen.blit(nutrients_img, (0, 0))

        if toggle_button1.draw():
            self.toggle1 = True
        else:
            self.toggle1 = False

        if toggle_button2.draw():
            self.toggle2 = True
        else:
            self.toggle2 = False

        if toggle_button3.draw():
            self.toggle3 = True
        else:
            self.toggle3 = False

        if toggle_button4.draw():
            self.toggle4 = True
        else:
            self.toggle4 = False

        if self.toggle1 or self.toggle2 or self.toggle3 or self.toggle4:
            if next_button.draw():
                self.next = True


class Times(Interface):
    def __init__(self):
        self.status = True
        self.toggle = False
        self.next = False

    def run(self, buttons: list):
        screen.fill((47, 82, 54))
        screen.blit(times_img, (0, 0))
        group = MultipleToggle(buttons)
        group.draw()

        if not group.allowed_toggle:
            for i in range(len(group.buttons)):
                if group.get_status()[i] is False:
                    group.buttons[i].set_allowed_click(False)
            self.toggle = True
        else:
            self.toggle = False

        if self.toggle:
            if next_button2.draw():
                self.next = True


class FoodDisplay(Interface):
    def __init__(self):
        self.status = True
        self.toggle1 = False
        self.toggle2 = False
        self.toggle3 = False
        self.toggle4 = False
        self.next = False
        self.first = True

    def run(self):
        screen.fill((47, 82, 54))

        if food_button1.draw():
            self.next = True
            return True
        if food_button2.draw():
            self.next = True
            return True
        if food_button3.draw():
            self.next = True
            return True
        if food_button4.draw():
            self.next = True
            return True
        if food_button5.draw():
            self.next = True
            return True




class ScreenManager:
    def __init__(self):
        self.active_screen = None

    def set_active_screen(self, screen):
        self.active_screen = screen

    def get_active_screen(self):
        return self.active_screen

    def update(self, inputs: Optional):
        if self.active_screen:
            if type(self.active_screen) in {Subcatergory, Difficulty, Serves, Times}:
                self.active_screen.run(inputs)
            else:
                self.active_screen.run()


main_menu = MainMenu()
subcat_menu = Subcatergory()
difficulty_menu = Difficulty()
serves_menu = Serves()
nutrients_menu = Nutrients()
time_menu = Times()
food_menu = FoodDisplay()
screen_manager = ScreenManager()
screen_manager.set_active_screen(main_menu)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if type(screen_manager.get_active_screen()) is Subcatergory:
        screen_manager.update(toggle_group1)
    elif type(screen_manager.get_active_screen()) is Difficulty:
        screen_manager.update(toggle_group2)
    elif type(screen_manager.get_active_screen()) is Serves:
        screen_manager.update(toggle_group3)
    elif type(screen_manager.get_active_screen()) is Times:
        screen_manager.update(toggle_group4)
    else:
        screen_manager.update(None)

    if main_menu.status:
        if main_menu.start:
            screen_manager.set_active_screen(subcat_menu)

    if subcat_menu.toggle:
        if subcat_menu.next:
            screen_manager.set_active_screen(difficulty_menu)
            subcat_menu.toggle = True
            subcat_menu.next = True

    if difficulty_menu.toggle:
        if difficulty_menu.next:
            screen_manager.set_active_screen(serves_menu)
            difficulty_menu.toggle = True
            difficulty_menu.next = True

    if serves_menu.toggle:
        if serves_menu.next:
            screen_manager.set_active_screen(time_menu)
            serves_menu.toggle = True
            serves_menu.next = True

    if time_menu.toggle:
        if time_menu.next:
            screen_manager.set_active_screen(food_menu)
            time_menu.toggle = True
            time_menu.next = True

    if food_menu.next:
        print('SAMPLE FOOD!')

    pygame.display.update()
pygame.display.quit()
pygame.quit()
sys.exit()
