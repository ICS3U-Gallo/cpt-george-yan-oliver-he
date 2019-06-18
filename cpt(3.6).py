import random
import arcade
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GAME_LENGTH = 4000

SCREEN_TITLE = "Flippy Bird"

MOVEMENT_SPEED = 3

temp_num = 1


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__("images/b1.png", 0.5)
        self.append_texture(arcade.load_texture("images/b2.png", scale=0.5))
        self.append_texture(arcade.load_texture("images/b3.png", scale=0.5))
        self.append_texture(arcade.load_texture("images/b4.png", scale=0.5))

        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2

    def update_animation(self):
        self.set_texture(temp_num // 4 % len(self.textures))


class Bg:
    def __init__(self):
        self.bg = arcade.Sprite("images/map2.png")
        self.bg.center_x = 1000 + SCREEN_WIDTH
        self.bg.center_y = 300

        self.bg2 = arcade.Sprite("images/map3.png")
        self.bg2.center_x = 3000 + SCREEN_WIDTH
        self.bg2.center_y = 300

    def draw(self):
        self.bg.draw()
        self.bg2.draw()


class MyGame(arcade.Window):
    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.bird = None
        self.wall_list = None
        self.physics_engine = None
        self.view_left = 0
        self.bg = None

        self.is_start = False
        self.is_over = False
        self.is_win = False

    def setup(self):

        self.is_start = False

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.bird = Bird()

        self.bg = Bg()

        for x in range(SCREEN_WIDTH + 100, GAME_LENGTH + SCREEN_WIDTH, 210):
            temp = []
            for y in range(0, 6):
                wall = arcade.Sprite("images/zhu1.png", 1.0)
                wall.center_x = x
                wall.center_y = y * 100 + 50
                temp.append(wall)
            temp.pop(random.randint(1, 4))

            for w in temp:
                self.wall_list.append(w)

        self.physics_engine = arcade.PhysicsEngineSimple(self.bird, self.wall_list)

        arcade.set_background_color(arcade.color.AMAZON)

        self.view_left = 0

    def on_draw(self):

        arcade.start_render()

        self.bg.draw()
        self.bird.draw()
        self.wall_list.draw()

        start_y = 400
        start_x = 100
        msg = "Good Luck !!"
        font_color = arcade.color.YELLOW

        if not self.is_start:
            msg = "Instructions:\n\nPress Space to start\n\nFailed when touch the bamboos"
            font_color = arcade.color.YELLOW

        if self.is_over:
            msg = "Game failed:\n\nPress Enter to Continue!!"
            font_color = arcade.color.BLACK

        if self.is_win:
            msg = "Victory!!\n\nPress Enter to continue!!"
            font_color = arcade.color.RED

        arcade.draw_text(msg, start_x, start_y, font_color, 24, font_name=("hkbd.ttf"))

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.bird.change_y1 = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.bird.change_y1 = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.bird.change_x1 = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.bird.change_x1 = MOVEMENT_SPEED

        if key == arcade.key.SPACE:
            self.bird.change_y = MOVEMENT_SPEED

            if not self.is_start and not self.is_over and not self.is_win:
                self.is_start = True

        if key == arcade.key.ENTER and self.is_over:
            if not self.is_start:
                self.is_start = True

        if key == arcade.key.ENTER and self.is_win:
            if not self.is_start:
                self.is_start = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.bird.change_y1 = 0

        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.bird.change_x1 = 0

        if key == arcade.key.SPACE:
            self.bird.change_y = -MOVEMENT_SPEED

    def update(self, delta_time):

        global temp_num
        temp_num += 1

        self.bird.update_animation()

        if not self.is_start:
            return

        self.physics_engine.update()
        self.view_left += 2
        self.bird.change_x = 2

        if (self.view_left > self.bird.center_x
                or self.bird.center_y < -10
                or self.bird.center_y > SCREEN_HEIGHT + 10):
            print("GAME OVER====")
            self.is_over = True
            self.is_win = False
            self.setup()

        if self.bird.center_x > GAME_LENGTH + SCREEN_WIDTH:
            print(" WINNING----")
            self.is_win = True
            self.is_over = False
            self.setup()

        arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, 0, SCREEN_HEIGHT)


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
