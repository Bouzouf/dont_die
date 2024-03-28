import pyglet
from pyglet import shapes
class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        image = pyglet.resource.image('ball.png')
        self.sprite = pyglet.sprite.Sprite(image, batch=self.batch)
    def on_draw(self):
        self.clear()
        # self.batch.draw()


ball_image = pyglet.image.load('ball.png')
ball = pyglet.sprite.Sprite(ball_image)
def main():
    batch = pyglet.graphics.Batch()
    image = pyglet.resource.image('ball.png')
    sprite1 = pyglet.sprite.Sprite(image, batch=batch)
    window = Window(width=640, height=480, caption='Pyglet')
    square = shapes.Rectangle(0, 0, window.width, window.height, color=(55, 55, 255))
    # Create a label
    label = pyglet.text.Label('Hello, world',
                            font_name='Times New Roman',
                            font_size=36,
                            x=window.width // 2, y=window.height // 2,
                            anchor_x='center', anchor_y='center')

    @window.event
    def on_draw():
        window.clear()
        # square.draw()  # Draw the square
        # label.draw()   # Draw the label
        # window.sprite.draw()
        batch.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        print('A key was pressed')
        ball.draw()
    pyglet.app.run()
main()
# Create a square shape



