import os.path

from vulk.baseapp import BaseApp
from vulk.graphic.texture import Texture
from vulk.graphic.d2.spritebatch import SpriteBatch


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()
        path = os.path.dirname(os.path.abspath(__file__))

        # self.spritebatch = SpriteBatch(self.context, clear=[1, 1, 1, 1])
        self.spritebatch = SpriteBatch(self.context)

        # ----------
        # TEST TEXTURE
        vulkan_path = os.path.join(path, 'vulkan.png')
        starwars_path = os.path.join(path, 'starwars.jpg')
        self.texture = Texture(self.context, vulkan_path)
        self.texture2 = Texture(self.context, starwars_path)
        self.x = 0
        self.y = 0
        self.size = 100

    def end(self):
        pass

    def render(self, delta):
        self.context.clear_final_image([1, 1, 1, 1])
        speed = 1
        self.x += speed * delta
        self.y += speed * delta
        self.size += speed * delta

        self.spritebatch.begin(self.context)
        self.spritebatch.draw(self.texture2, 0, 0, self.size, self.size)
        self.spritebatch.draw(self.texture, self.context.width - self.size,
                              0, self.size, self.size)
        spritebatch_semaphore = self.spritebatch.end()

        self.context.swap([spritebatch_semaphore])
