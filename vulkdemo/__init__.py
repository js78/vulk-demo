from os import path

from vulk.baseapp import BaseApp
from vulk.graphic.texture import Texture
from vulk.graphic.d2.spritebatch import SpriteBatch
from vulk.graphic.camera import OrthographicCamera
from vulk.math.shape import Rectangle
from vulk import audio


ASSET = path.join(path.dirname(path.abspath(__file__)), 'asset')


def asset(name):
    return path.join(ASSET, name)


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()

        # Load images
        self.drop_image = Texture(self.context, asset('droplet.png'))
        self.bucket_image = Texture(self.context, asset('bucket.png'))

        # Load sounds
        self.drop_sound = audio.Sound(asset('drop.wav'))
        self.rain_music = audio.Music(asset('rain.mp3'))

        # Start immediatly background music
        self.rain_music.play(repeat=0)

        # Initialize camera and spritebatch
        self.camera = OrthographicCamera(800, 480)
        self.camera.update()
        self.spritebatch = SpriteBatch(self.context)

        # Shapes
        self.bucket = Rectangle(800 / 2 - 64 / 2, 480 - 20 - 64, 64, 64)

    def end(self):
        pass

    def render(self, delta):
        # Clear screen
        self.context.clear_final_image([0, 0, 0.2, 1])

        # Update camera
        self.camera.update()

        # Render with sprtebatch
        self.spritebatch.update_projection(self.camera.combined)
        self.spritebatch.begin(self.context)
        self.spritebatch.draw(self.bucket_image, self.bucket.x, self.bucket.y)
        spritebatch_semaphore = self.spritebatch.end()

        self.context.swap([spritebatch_semaphore])
