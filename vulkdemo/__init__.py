import os.path

from vulk.baseapp import BaseApp
from vulk.graphic.texture import Texture
from vulk.graphic.d2.spritebatch import SpriteBatch


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        path = os.path.dirname(os.path.abspath(__file__))

        self.spritebatch = SpriteBatch(self.context)

        # ----------
        # TEST TEXTURE
        self.texture = Texture(self.context, os.path.join(path, 'vulkan.png'))
        self.x = 0
        self.y = 0

    def end(self):
        pass

    def render(self, delta):
        speed = 1
        self.x += speed * delta
        self.y += speed * delta

        self.spritebatch.begin(self.context)
        self.spritebatch.draw(self.texture, self.x, self.y, 100, 100)
        spritebatch_semaphore = self.spritebatch.end(self.context)

        self.context.swap([spritebatch_semaphore])
