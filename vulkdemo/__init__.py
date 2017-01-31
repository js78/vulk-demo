import os.path

from vulk.baseapp import BaseApp
from vulk.graphic.texture import Texture, TextureRegion
from vulk.graphic.d2.spritebatch import SpriteBatch
from vulk import audio


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'asset')

        # self.spritebatch = SpriteBatch(self.context, clear=[1, 1, 1, 1])
        self.spritebatch = SpriteBatch(self.context)

        # ----------
        # TEST TEXTURE
        vulkan_path = os.path.join(path, 'vulkan.png')
        starwars_path = os.path.join(path, 'starwars.jpg')
        texture = Texture(self.context, vulkan_path)
        self.texture2 = Texture(self.context, starwars_path)
        self.region1 = TextureRegion(texture, u=0.3, u2=0.7)
        self.x = 0
        self.y = 0
        self.size = 100
        s = audio.Music(os.path.join(path, '28283__acclivity__undertreeinrain.mp3'))
        s.play()

    def end(self):
        pass

    def render(self, delta):
        self.context.clear_final_image([1, 1, 1, 1])
        speed = 1
        self.x += speed * delta
        self.y += speed * delta
        self.size += speed * delta

        self.spritebatch.begin(self.context)
        self.spritebatch.draw_region(self.region1, 0, 0, self.size, self.size)
        spritebatch_semaphore = self.spritebatch.end()

        self.context.swap([spritebatch_semaphore])
