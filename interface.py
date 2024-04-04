"""
Main interface of the app
"""
from typing import Any, Optional

import io
import textwrap
import webbrowser
import requests
import pygame
import graphs

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 700
GROBOLD = 'assets/GROBOLD.ttf'
MONTSERRAT = 'assets/Montserrat-SemiBold.ttf'
HELVETICA = 'assets/Helvetica-Bold.ttf'


class MultipleToggle:
    """
    Multiple toggle buttons Instance
    """
    buttons: list
    status: bool
    allowed_toggle: bool

    def __init__(self, buttons: list) -> None:
        self.buttons = buttons
        if any([button.clicked is True for button in self.buttons]):
            self.status = True
        else:
            self.status = False
        if self.status is True:
            self.allowed_toggle = False
        else:
            self.allowed_toggle = True

    def get_status(self) -> list:
        """
        returns the clicked status of the button
        """
        return [button.clicked for button in self.buttons]

    def get_clicked(self) -> Any:
        """
        Returns the clicked button
        """
        for button in self.buttons:
            if button.clicked:
                return button
        return None

    def get_allowed_toggle(self) -> bool:
        """
        returns the allowance of the button to be toggled
        """
        return self.allowed_toggle

    def update_toggle_state(self, toggled_button: Any) -> None:
        """
        Ensures only the toggled_button remains toggled, untoggling others.
        """
        for button in self.buttons:
            if button != toggled_button:
                button.untoggle()

    def draw(self) -> None:
        """
        draws the button on to the screen
        """
        for button in self.buttons:
            button.draw()


def run_game() -> None:
    """
    Runs the main pygame interface
    """
    logo_img = pygame.image.load('assets/logo.png')

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('FOOD MOOD')
    pygame.display.set_icon(logo_img)

    small_font_size = 14
    medium_font_size = 20

    # Load the custom font
    font_montserrat_medium = pygame.font.Font(MONTSERRAT, medium_font_size)
    font_helvetica_small = pygame.font.Font(HELVETICA, small_font_size)

    # Buttons
    next_img = pygame.image.load('assets/buttons/next_btn.png').convert_alpha()
    food_img = pygame.image.load('assets/buttons/food_btn.png').convert_alpha()
    food_name_img = pygame.image.load('assets/buttons/food_name_btn.png').convert_alpha()
    food_desc_img = pygame.image.load('assets/buttons/food_desc_btn.png').convert_alpha()
    recipe_img = pygame.image.load('assets/buttons/recipe_btn.png').convert_alpha()
    back_img = pygame.image.load('assets/buttons/back_btn.png').convert_alpha()
    close_img = pygame.image.load('assets/buttons/close_btn.png').convert_alpha()
    back_img_food = pygame.image.load('assets/buttons/back_btn_food.png').convert_alpha()
    next_img_food = pygame.image.load('assets/buttons/next_btn_food.png').convert_alpha()

    # Buttons Hover
    next_img_hover = pygame.image.load('assets/buttons/next_btn_hover.png').convert_alpha()
    food_img_hover = pygame.image.load('assets/buttons/food_btn_hover.png').convert_alpha()
    recipe_img_hover = pygame.image.load('assets/buttons/recipe_btn_hover.png').convert_alpha()
    back_img_hover = pygame.image.load('assets/buttons/back_btn_hover.png').convert_alpha()
    close_img_hover = pygame.image.load('assets/buttons/close_btn_hover.png').convert_alpha()
    back_img_food_hover = pygame.image.load('assets/buttons/back_btn_food_hover.png').convert_alpha()
    next_img_food_hover = pygame.image.load('assets/buttons/next_btn_food_hover.png').convert_alpha()

    # Toggle Buttons
    toggle_img = pygame.image.load('assets/buttons/toggle_btn.png').convert_alpha()
    toggle_clicked_img = pygame.image.load('assets/buttons/toggle_btn_clicked.png').convert_alpha()
    toggle_hover_img = pygame.image.load('assets/buttons/toggle_btn_hover.png').convert_alpha()
    toggle_hover_clicked_img = pygame.image.load('assets/buttons/toggle_btn_clicked_hover.png').convert_alpha()

    subcat_img = pygame.image.load('assets/subcat_bg.png')
    difficult_img = pygame.image.load('assets/difficulty_bg.png')
    serves_img = pygame.image.load('assets/servings_bg.png')
    times_img = pygame.image.load('assets/time_bg.png')
    food_bg = pygame.image.load('assets/food_bg.png')
    last_bg = pygame.image.load('assets/last_bg.png')

    bg_img2 = pygame.image.load('assets/bg_img3.png')
    bg_img_food = pygame.image.load('assets/bg_img_food.png')
    nofood_img = pygame.image.load('assets/nofood.png')
    logo_home = pygame.image.load('assets/logo.png')
    logo_home_hover = pygame.image.load('assets/logo_hover.png')

    class Button:
        """Button Instance"""
        name: str
        x: int
        y: int
        image: pygame.Surface
        image_pressed: pygame.Surface
        scale: float
        clicked: bool
        rect: pygame.rect

        def __init__(self, name: str, x: int, y: int, image: pygame.Surface, image_pressed: pygame.Surface,
                     scale: float) -> None:
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.smoothscale(image, (int(width) * scale, int(height) * scale))
            self.image_pressed = pygame.transform.smoothscale(image_pressed,
                                                              (int(width) * scale, int(height) * scale))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False
            self.name = name

        def draw(self) -> bool:
            """
                Draws
            """
            action = False
            # get mouse position
            pos = pygame.mouse.get_pos()

            # check mouse is over and clicked condition
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
        """Modifided button Instance to be able to be toggled on and offs"""
        name: str
        x: int
        y: int
        image: pygame.Surface
        image_hover: pygame.Surface
        image_pressed: pygame.Surface
        image_pressed_hover: pygame.Surface
        scale_norm: float
        scale_pressed: float
        rect: pygame.rect
        multiple_toggle_instance: MultipleToggle | None
        clicked: bool
        click_pending: bool

        def __init__(self, name: str, x: int, y: int, image: pygame.Surface, image_hover: pygame.Surface,
                     image_pressed: pygame.Surface, image_pressed_hover: pygame.Surface, scale_norm: float,
                     scale_pressed: float) -> None:
            super().__init__(name, x, y, image, image_pressed, scale_norm)
            self.multiple_toggle_instance = None
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.smoothscale(image, (int(width * scale_norm), int(height * scale_norm)))
            self.image_hover = pygame.transform.smoothscale(image_hover,
                                                            (int(width * scale_norm), int(height * scale_norm)))
            self.image_pressed = pygame.transform.smoothscale(image_pressed,
                                                              (int(width * scale_pressed),
                                                               int(height * scale_pressed)))
            self.image_pressed_hover = pygame.transform.smoothscale(image_pressed_hover,
                                                                    (int(width * scale_pressed),
                                                                     int(height * scale_pressed)))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.clicked = False
            self.click_pending = False  # To track if a click is in process
            self.name = name

        def set_multiple_toggle(self, multiple_toggle_instance: MultipleToggle) -> None:
            """
            Set the multipletoggle instance for toggle buttons
            """
            self.multiple_toggle_instance = multiple_toggle_instance

        def draw(self) -> bool:
            pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            if self.rect.collidepoint(pos) and self.multiple_toggle_instance is not None:
                if mouse_pressed and not self.click_pending:
                    self.click_pending = True  # Mark that a click started
                elif not mouse_pressed and self.click_pending:
                    # Toggle logic
                    self.clicked = not self.clicked
                    if self.clicked:  # If toggled, update state in MultipleToggle
                        self.multiple_toggle_instance.update_toggle_state(self)
                    self.click_pending = False  # Reset click tracking
                    # print(f'{self.name} is Toggled' if self.clicked else f'{self.name} is untoggled')

            if self.rect.collidepoint(pos):
                if mouse_pressed and not self.click_pending:
                    self.click_pending = True  # Mark that a click started
                elif not mouse_pressed and self.click_pending:
                    # Only toggle if the mouse was clicked and then released while over the button
                    self.clicked = not self.clicked
                    self.click_pending = False  # Reset click tracking
                    # print(f'{self.name} is Toggled' if self.clicked else f'{self.name} is untoggled')

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

        def set_allowed_click(self, allow: bool) -> None:
            """
            set when a click is allowed
            """
            self.click_pending = allow

        def untoggle(self) -> None:
            """
            Sets the button's clicked state to False.
            """
            self.clicked = False
            # print(f'{self.name} is untoggled')

    class TextButton(Button):
        """Button with text, image, and star rating that changes text color on hover."""
        name: str
        x: int
        y: int
        image: pygame.Surface
        image_pressed: pygame.Surface
        scale: float
        text: str
        font: pygame.font.Font
        text_color: tuple[int, int, int]
        current_text_color: tuple[int, int, int]
        text_surface: pygame.Surface
        text_x: int
        text_y: int

        def __init__(self, name: str, x: int, y: int, image: pygame.Surface, image_pressed: pygame.Surface,
                     scale: float,
                     text: str, font: pygame.font.Font, text_color: tuple[int, int, int]) -> None:
            super().__init__(name, x, y, image, image_pressed, scale)
            self.text = text
            self.font = font
            self.text_color = text_color

            # Initial text color
            self.current_text_color = text_color
            # Render the text
            self.text_surface = self.font.render(self.text, True, self.current_text_color)
            # Calculate text position to center it on the button, adjusting for the left image
            self.text_x = self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2
            self.text_y = self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2

        def draw(self) -> bool:
            """
            Draws the button, text, and star rating on top of it within the button bounds.
            Adjusts the text color based on mouse hover.
            """  # Assuming 'screen' is defined globally

            action = super().draw()  # Call the draw method of the base class to draw the button
            screen.blit(self.text_surface, (self.text_x, self.text_y))
            return action

    class TextImageButton(Button):
        """Button with text, image, and star rating that changes text color on hover."""
        ame: str
        x: int
        y: int
        image: pygame.Surface
        image_pressed: pygame.Surface
        scale: float
        text: str
        font: pygame.font.Font
        text_color: tuple[int, int, int]
        text_hover_color: tuple[int, int, int]
        current_text_color: tuple[int, int, int]
        rating: int
        left_image: pygame.Surface
        star_full: pygame.Surface
        star_empty: pygame.Surface
        text_surface: pygame.Surface
        text_x: int
        text_y: int

        def __init__(self, name: str, x: int, y: int, image: pygame.Surface, image_pressed: pygame.Surface,
                     scale: float,
                     text: str, font: pygame.font.Font, text_color: tuple[int, int, int],
                     text_hover_color: tuple[int, int, int], rating: int, left_image: pygame.Surface) -> None:
            super().__init__(name, x, y, image, image_pressed, scale)
            self.text = text
            self.font = font
            self.text_color = text_color
            self.text_hover_color = text_hover_color
            self.rating = rating  # Integer rating from 1 to 5
            try:
                self.left_image = pygame.transform.smoothscale(left_image, (80, 80))
            except ValueError:
                self.left_image = pygame.transform.scale(left_image, (80, 80))
                # Load the image to display to the left of the text
            self.star_full = pygame.image.load('assets/buttons/stars_full.png')  # Load your full star image
            self.star_empty = pygame.image.load('assets/buttons/stars_empty.png')  # Load your empty star image

            # Initial text color
            self.current_text_color = text_color
            # Render the text
            self.text_surface = self.font.render(self.text, True, self.current_text_color)
            # Calculate text position to center it on the button, adjusting for the left image
            self.text_x = self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2
            self.text_y = self.rect.y + (self.rect.height - self.text_surface.get_height()
                                         - self.star_full.get_height()) // 2

        def draw(self) -> bool:
            """
            Draws the button, text, and star rating on top of it within the button bounds.
            Adjusts the text color based on mouse hover.
            """

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
            stars_x_base = self.text_x + (self.text_surface.get_width() - 5 * self.star_full.get_width() - 4 * 5) / 2
            # Center stars relative to text
            for i in range(5):
                star_x = stars_x_base + i * (self.star_full.get_width() + 5)  # Adjust spacing as needed
                star_y = self.text_y + self.text_surface.get_height() + 5  # Position stars just below the text
                if i < self.rating:
                    screen.blit(self.star_full, (star_x, star_y))
                else:
                    screen.blit(self.star_empty, (star_x, star_y))

            return action

    class ButtonDescription(Button):
        """Extended Button class with text description capability that wraps text to fit inside the button."""
        name: str
        x: int
        y: int
        image: pygame.Surface
        image_pressed: pygame.Surface
        scale: float
        description: str
        font: pygame.font.Font
        font_path: str
        font_size: int
        text_color: tuple[int, int, int]
        text_surfaces: list
        text_start_y: int

        def __init__(self, name: str, x: int, y: int, image: pygame.Surface, image_pressed: pygame.Surface,
                     scale: float, description: str, font_path: str, font_size: int, text_color: tuple[int, int, int]) \
                -> None:
            super().__init__(name, x, y, image, image_pressed, scale)
            self.description = description
            self.font_path = font_path
            self.font_size = font_size
            self.text_color = text_color

            # Load the font
            self.font = pygame.font.Font(font_path, font_size)

            # Initialize an empty list to hold rendered text surfaces and their positions
            self.text_surfaces = []
            self.render_wrapped_text(description, 700)  # Pass the available width for text

        def render_wrapped_text(self, text: str, available_width: int) -> None:
            """Renders wrapped text to fit inside the button."""
            # Estimate average character width for the current font and size
            average_char_width = self.font.size("A")[0]
            max_chars_per_line = max(1, available_width // average_char_width)

            # Use textwrap to wrap the text based on estimated max chars per line
            wrapped_text = textwrap.wrap(text, width=max_chars_per_line)

            # Clear any existing text surfaces
            self.text_surfaces.clear()

            # Render each line of wrapped text and store its surface
            total_text_height = 0
            for line in wrapped_text:
                text_surface = self.font.render(line, True, self.text_color)
                self.text_surfaces.append(text_surface)
                total_text_height += text_surface.get_height()

            # Adjust starting y position to vertically center the block of text
            self.text_start_y = self.rect.y + (self.rect.height - total_text_height) // 2

        def draw(self) -> bool:
            """
            Draws the button and the wrapped text description on top of it, ensuring it fits within the button.
            """
            action = super().draw()

            # Draw each line of wrapped text
            current_y = self.text_start_y
            for text_surface in self.text_surfaces:
                text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
                screen.blit(text_surface, (text_x, current_y))
                current_y += text_surface.get_height()

            return action

    class ButtonWithLink(Button):
        """Button Instance"""
        name: str
        x: int
        y: int
        image: pygame.Surface
        image_pressed: pygame.Surface
        scale: float
        link: str

        def __init__(self, name: str, x: int, y: int, image: pygame.Surface, image_pressed: pygame.Surface,
                     scale: float,
                     link: str) -> None:
            super().__init__(name, x, y, image, image_pressed, scale)
            self.link = link

        def draw(self) -> bool:
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

        def get_link(self) -> str:
            """
            returns the link associated with the button
            """
            return self.link

    # start_button = Button('start_btn', 230, 230, start_img, start_img_hover, 1)
    start_button = Button('start_btn', 150, 230, logo_home, logo_home_hover, 1)
    next_button2 = Button('next_btn2', 500, 620, next_img, next_img_hover, 1 / 2)
    back_button = Button('back_btn', 10, 20, back_img, back_img_hover, 1)
    close_button = Button('close_btn', 550, 20, close_img, close_img_hover, 1)
    back_button_food = Button('back_btn', 430, 640, back_img_food, back_img_food_hover, 1)
    next_button_food = Button('back_btn', 550, 640, next_img_food, next_img_food_hover, 1)

    toggle_button5 = Toggle('Vegan Recipes', 100, 410, toggle_img, toggle_hover_img, toggle_clicked_img,
                            toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button6 = Toggle('Recipes with Animal Products', 100, 210, toggle_img, toggle_hover_img,
                            toggle_clicked_img, toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button7 = Toggle('Vegetarian Recipes', 100, 310, toggle_img, toggle_hover_img,
                            toggle_clicked_img, toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button8 = Toggle('Miscellaneous', 100, 510, toggle_img, toggle_hover_img, toggle_clicked_img,
                            toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button9 = Toggle('Challenging', 100, 210, toggle_img, toggle_hover_img, toggle_clicked_img,
                            toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button10 = Toggle('Easy', 100, 110, toggle_img, toggle_hover_img, toggle_clicked_img,
                             toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button13 = Toggle('5+', 100, 310, toggle_img, toggle_hover_img, toggle_clicked_img,
                             toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button14 = Toggle('1 ~ 2', 100, 110, toggle_img, toggle_hover_img, toggle_clicked_img,
                             toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button15 = Toggle('3 ~ 4', 100, 210, toggle_img, toggle_hover_img, toggle_clicked_img,
                             toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button21 = Toggle('Lengthy (40 ~ 60 mins)', 100, 310, toggle_img, toggle_hover_img,
                             toggle_clicked_img, toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button22 = Toggle('Quick (0 ~ 20 mins)', 100, 110, toggle_img, toggle_hover_img,
                             toggle_clicked_img, toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button23 = Toggle('Moderate (20 ~ 40 mins)', 100, 210, toggle_img, toggle_hover_img,
                             toggle_clicked_img, toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button24 = Toggle('More than 1 hr', 100, 410, toggle_img, toggle_hover_img,
                             toggle_clicked_img, toggle_hover_clicked_img, 1 / 2, 1 / 2)
    toggle_button25 = Toggle('Meal-Specific Recipes', 100, 110, toggle_img, toggle_hover_img,
                             toggle_clicked_img, toggle_hover_clicked_img, 1 / 2, 1 / 2)

    toggle_group1 = [toggle_button5, toggle_button6, toggle_button7, toggle_button8, toggle_button25]
    toggle_group2 = [toggle_button9, toggle_button10]
    toggle_group3 = [toggle_button13, toggle_button14, toggle_button15]
    toggle_group5 = [toggle_button21, toggle_button22, toggle_button23, toggle_button24]

    all_foods = graphs.build_graph('recipes.json')

    outputs = []
    recommended_foods = []

    class Interface:
        """
        Interface Instance
        """
        status: bool

        def __init__(self) -> None:
            self.status = True

    class MainMenu(Interface):
        """
        Main Menu Interface Instance (Logo Menu)
        """
        status: bool
        start: bool
        option: bool

        def __init__(self) -> None:
            super().__init__()
            self.status = True
            self.start = False
            self.option = False

        def run(self) -> None:
            """
            runs the interface
            """
            screen.blit(bg_img2, (0, 0))
            # screen.fill((43, 191, 27))

            if start_button.draw():
                self.start = True

    class Subcatergory(Interface):
        """
        Subcatergory Interface Instance
        """
        status: bool
        toggle: bool
        next: bool

        def __init__(self) -> None:
            super().__init__()
            self.status = True
            self.toggle = False
            self.next = False

        def run(self, buttons: list) -> None:
            """
            runs the interface
            """
            screen.fill((95, 167, 118))
            screen.blit(subcat_img, (0, 0))
            group = MultipleToggle(buttons)
            group.draw()

            for button in group.buttons:
                button.set_multiple_toggle(group)

            if not group.get_allowed_toggle():
                self.toggle = True
            else:
                self.toggle = False

            if self.toggle:
                if next_button2.draw():
                    outputs.append(group.get_clicked().name)
                    self.next = True

    class Difficulty(Interface):
        """
        Difficulty Interface Instance
        """
        status: bool
        toggle: bool
        next: bool

        def __init__(self) -> None:
            super().__init__()
            self.status = True
            self.toggle = False
            self.next = False

        def run(self, buttons: list) -> None:
            """
            runs the interface
            """
            screen.fill((43, 191, 27))
            screen.blit(difficult_img, (0, 0))
            group = MultipleToggle(buttons)
            group.draw()

            for button in group.buttons:
                button.set_multiple_toggle(group)

            if not group.get_allowed_toggle():
                self.toggle = True
            else:
                self.toggle = False

            if self.toggle:
                if next_button2.draw():
                    outputs.append(group.get_clicked().name)
                    self.next = True

    class Serves(Interface):
        """
        Serves selector Interface Instance
        """
        status: bool
        toggle: bool
        next: bool

        def __init__(self) -> None:
            super().__init__()
            self.status = True
            self.toggle = False
            self.next = False

        def run(self, buttons: list) -> None:
            """
            runs the interface
            """
            screen.fill((43, 191, 27))
            screen.blit(serves_img, (0, 0))
            group = MultipleToggle(buttons)
            group.draw()

            for button in group.buttons:
                button.set_multiple_toggle(group)

            if not group.get_allowed_toggle():
                self.toggle = True
            else:
                self.toggle = False

            if self.toggle:
                if next_button2.draw():
                    outputs.append(group.get_clicked().name)
                    self.next = True

    class Times(Interface):
        """
        Cooking Time selector Interface Instance
        """
        status: bool
        toggle: bool
        next: bool

        def __init__(self) -> None:
            super().__init__()
            self.status = True
            self.toggle = False
            self.next = False

        def run(self, buttons: list) -> None:
            """
            runs the interface
            """
            screen.fill((43, 191, 27))
            screen.blit(times_img, (0, 0))
            group = MultipleToggle(buttons)
            group.draw()

            for button in group.buttons:
                button.set_multiple_toggle(group)

            if not group.get_allowed_toggle():
                self.toggle = True
            else:
                self.toggle = False

            if self.toggle:
                if next_button2.draw():
                    outputs.append(group.get_clicked().name)
                    recommended_foods.extend(all_foods.get_food_options(outputs))
                    print('#' * 50)
                    print('Final Choices:')
                    for output in outputs:
                        print(output)
                    print('#' * 50)
                    self.next = True

    class FoodDisplay(Interface):
        """Foods Interface Instance"""
        status: bool
        toggle1: bool
        toggle2: bool
        toggle3: bool
        toggle4: bool
        food: bool
        next: bool
        back: bool
        first: bool
        num: int | None
        total_page: int | None
        button: list
        chosen_button: TextImageButton | None
        chosen_desc: str | None
        chosen_url: str | None

        def __init__(self) -> None:
            super().__init__()
            self.status = True
            self.toggle1 = False
            self.toggle2 = False
            self.toggle3 = False
            self.toggle4 = False
            self.food = False
            self.next = False
            self.back = False
            self.first = True
            self.num = None
            self.total_page = None
            self.chosen_desc = None
            self.chosen_url = None
            self.chosen_button = None

        def make_button(self, rec_food: list) -> None:
            """
            Makes the button isntance for the specific food interface
            """
            temp_list = []
            for i in range(len(rec_food)):
                x = 50
                y = 0
                if i == 0:
                    y += 70
                elif i == 1:
                    y += 185
                elif i == 2:
                    y += 300
                elif i == 3:
                    y += 415
                elif i == 4:
                    y += 530
                if len(rec_food[i].item) > 50:
                    text = f'{rec_food[i].item[50:]} ...'
                else:
                    text = rec_food[i].item
                text_color = (255, 255, 255)
                text_hover_color = (0, 0, 0)
                rating = rec_food[i].rating
                r = requests.get(rec_food[i].image)
                img = io.BytesIO(r.content)
                left_image = pygame.image.load(img)
                try:
                    left_image = pygame.transform.smoothscale(left_image, (80, 80))
                except ValueError:
                    left_image = pygame.transform.scale(left_image, (80, 80))
                temp_list.append(TextImageButton(f'food{i}', x, y, food_img, food_img_hover, 1, text,
                                                 font_helvetica_small, text_color, text_hover_color, rating, left_image)
                                 )
            self.button = temp_list

        def set_num(self, num: int) -> None:
            """
            set the number of the current page of the interface
            """
            self.num = num

        def set_total_page(self, page: int) -> None:
            """
            set the number of total pages of the interface
            """
            self.total_page = page

        def run(self, rec_food: list) -> bool:
            """
            runs the interface
            """
            # screen.fill((43, 191, 27))
            screen.blit(food_bg, (0, 0))

            # if any(food.draw for food in self.button):
            for i in range(len(self.button)):
                if self.button[i].draw():
                    self.food = True
                    self.chosen_button = self.button[i]
                    self.chosen_desc = rec_food[i].description
                    self.chosen_url = rec_food[i].url
                    return True
            if len(self.button) == 0:
                screen.blit(nofood_img, (0, 0))
                return False

            if self.num > 1:
                if back_button_food.draw():
                    self.back = True

            else:
                if self.total_page > 1:
                    if next_button_food.draw():
                        self.next = True
                else:
                    return False

            if self.num < self.total_page:
                if next_button_food.draw():
                    self.next = True
                    return True
                return False
            else:
                if back_button_food.draw():
                    self.back = True
                    return True
                return False

        def get_chosen(self) -> TextImageButton:
            """
            returns the chosen button
            """
            return self.chosen_button

        def get_chosen_desc(self) -> str:
            """
            returns the chosen button's description
            """
            return self.chosen_desc

        def get_chosen_url(self) -> str:
            """
            returns the chosen button's url
            """
            return self.chosen_url

    class FoodIndividual(Interface):
        """The interface after a food was selected"""
        next: bool
        back: bool
        link: str

        def __init__(self) -> None:
            super().__init__()
            self.next = False
            self.back = False

        def run(self, chosen_food: TextImageButton, chosen_food_desc: str, chosen_food_url: str) -> None:
            """
            runs the interface
            """
            # screen.fill((43, 191, 27))
            screen.blit(bg_img_food, (0, 0))
            food_image = chosen_food.left_image
            try:
                food_image_scaled = pygame.transform.smoothscale(food_image, (250, 250))
            except ValueError:
                food_image_scaled = pygame.transform.scale(food_image, (250, 250))
            screen.blit(food_image_scaled, (225, 50))
            food_name_btn = TextButton('foodname', 135, 300, food_name_img, food_name_img, 1,
                                       chosen_food.text, font_montserrat_medium, (0, 0, 0))
            food_desc = ButtonDescription('Desc', 60, 350, food_desc_img, food_desc_img,
                                          1, chosen_food_desc, HELVETICA, 14, (182, 182, 182))
            recipe = ButtonWithLink('recipe link', 230, 620, recipe_img, recipe_img_hover, 1,
                                    chosen_food_url)
            food_name_btn.draw()
            food_desc.draw()
            if recipe.draw():
                self.next = True
                self.link = recipe.link
            if back_button.draw():
                self.back = True
            return None

    class Closing(Interface):
        """
        Closing page Interface Instance
        """
        next: bool

        def __init__(self) -> None:
            super().__init__()
            self.next = False

        def run(self) -> None:
            """
            runs the interface
            """
            screen.blit(last_bg, (0, 0))
            if close_button.draw():
                self.next = True
            return None

    class ScreenManager:
        """
        Instance that manages the screen in pygame
        """
        active_screen: (Interface | MainMenu | Subcatergory | Difficulty
                        | Serves | Times | FoodDisplay | FoodIndividual | Closing | None)

        def __init__(self) -> None:
            self.active_screen = None

        def set_active_screen(self, current_screen: Interface) -> None:
            """
            sets the status of the active screen
            """
            self.active_screen = current_screen

        def get_active_screen(self) -> Interface:
            """
            return the current active screen
            """
            return self.active_screen

        def update(self, inputs: Any = None, input2: Optional[Any] = None, input3: Optional[Any] = None) -> None:
            """
            updates the current active screen
            """
            if self.active_screen:
                if type(self.active_screen) in {Subcatergory, Difficulty, Serves, Times, FoodDisplay}:
                    self.active_screen.run(inputs)
                elif isinstance(self.active_screen, FoodIndividual):
                    self.active_screen.run(inputs, input2, input3)
                else:
                    self.active_screen.run()

    # IMPORTANT
    # for the interface to work it needs to be given a list with the length of exactly 5.

    main_menu = MainMenu()
    subcat_menu = Subcatergory()
    difficulty_menu = Difficulty()
    serves_menu = Serves()
    time_menu = Times()
    food_menu = FoodDisplay()

    food_menu2 = FoodDisplay()

    recipe_menu = FoodIndividual()
    recipe_menu2 = FoodIndividual()
    closing_menu = Closing()

    screen_manager = ScreenManager()
    screen_manager.set_active_screen(main_menu)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Set run to False to exit the main loop

        active_screen = screen_manager.get_active_screen()

        # Update screen based on the active screen type
        if isinstance(active_screen, Subcatergory):
            screen_manager.update(toggle_group1)
        elif isinstance(active_screen, Difficulty):
            screen_manager.update(toggle_group2)
        elif isinstance(active_screen, Serves):
            screen_manager.update(toggle_group3)
        elif isinstance(active_screen, Times):
            screen_manager.update(toggle_group5)
        elif isinstance(active_screen, FoodDisplay):
            if screen_manager.get_active_screen() is food_menu:
                screen_manager.update(recommended_foods[:5])
            if screen_manager.get_active_screen() is food_menu2:
                screen_manager.update(recommended_foods[5:10])
        elif isinstance(active_screen, FoodIndividual):
            if screen_manager.get_active_screen() is recipe_menu:
                screen_manager.update(food_menu.get_chosen(), food_menu.get_chosen_desc(), food_menu.get_chosen_url())
            if screen_manager.get_active_screen() is recipe_menu2:
                screen_manager.update(food_menu2.get_chosen(), food_menu2.get_chosen_desc(),
                                      food_menu2.get_chosen_url())
        else:
            screen_manager.update(None)

        # Main menu logic
        if main_menu.status and main_menu.start:
            main_menu.status = False
            screen_manager.set_active_screen(subcat_menu)

        # Subcategory menu logic
        if subcat_menu.toggle and subcat_menu.next:
            subcat_menu.toggle = False
            screen_manager.set_active_screen(difficulty_menu)

        # Difficulty menu logic
        if difficulty_menu.toggle and difficulty_menu.next:
            difficulty_menu.toggle = False
            screen_manager.set_active_screen(serves_menu)

        # Serves menu logic
        if serves_menu.toggle and serves_menu.next:
            serves_menu.toggle = False
            screen_manager.set_active_screen(time_menu)

        # Time menu logic
        if time_menu.toggle and time_menu.next:
            time_menu.toggle = False
            food_menu.set_num(1)
            if len(recommended_foods) > 5:
                food_menu.set_total_page(2)
                food_menu.set_total_page(2)
                food_menu2.set_num(2)
                food_menu2.set_total_page(2)
                food_menu2.make_button(recommended_foods[5:10])
            else:
                food_menu.set_total_page(1)
            food_menu.make_button(recommended_foods[:5])
            screen_manager.set_active_screen(food_menu)

        # Food menu logic
        if food_menu.food:
            food_menu.food = False
            screen_manager.set_active_screen(recipe_menu)

        if food_menu.next:
            food_menu.next = False
            screen_manager.set_active_screen(food_menu2)

        if food_menu2.back:
            food_menu2.back = False
            screen_manager.set_active_screen(food_menu)

        if food_menu2.food:
            food_menu2.food = False
            screen_manager.set_active_screen(recipe_menu2)

        # Recipe menu logic
        if recipe_menu.next:
            webbrowser.open(recipe_menu.link)
            recipe_menu.next = False
            screen_manager.set_active_screen(closing_menu)

        if recipe_menu.back:
            recipe_menu.next = False
            recipe_menu.back = False
            screen_manager.set_active_screen(food_menu)

        if recipe_menu2.next:
            webbrowser.open(recipe_menu2.link)
            recipe_menu2.next = False
            screen_manager.set_active_screen(closing_menu)

        if recipe_menu2.back:
            recipe_menu2.next = False
            recipe_menu2.back = False
            screen_manager.set_active_screen(food_menu2)

        if closing_menu.next:
            pygame.quit()
            run = False
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['textwrap', 'webbrowser', 'io', 'requests', 'pygame', 'graphs'],
        'allowed-io': ['untoggle', 'draw', 'run', 'run_game'],
        'max-line-length': 120
    })
