import sweeperlib
import logic


def draw_field():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """
    # 40x40 pixel
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    for y, row in enumerate(logic.state["field"]):
        for x, square in enumerate(row):
            sweeperlib.prepare_sprite(square, x * 40, y * 40)

    sweeperlib.draw_sprites()

def mouse_handler(x, y, mouse_button, button_modifier):
    """
    This function is called when a mouse button is clicked inside the game window.
    Prints the position and clicked button of the mouse to the terminal.
    """
    logic.click_detection(x, y, mouse_button)

def main():
    """
    Loads the game graphics, creates a game window and sets a draw handler for it.
    """

    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(len(logic.state["field"][0]) * 40, len(logic.state["field"]) * 40)
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.set_mouse_handler(mouse_handler)
    sweeperlib.start()

