import os.path
import random

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

    def end(self):
        pass

    def render(self, delta):
        self.spritebatch.begin(self.context)

        self.spritebatch.draw(self.texture, 0, 0)
        self.spritebatch.draw(self.texture, 100, 100)
        self.spritebatch.draw(self.texture, 200, 200)
        spritebatch_semaphore = self.spritebatch.end(self.context)

        self.context.swap([spritebatch_semaphore])
