#!/usr/bin/env python3.6
from os import path
import random

from vulk.baseapp import BaseApp
from vulk.graphic.texture import Texture
from vulk.graphic.d2.batch import SpriteBatch
from vulk.graphic.camera import OrthographicCamera
from vulk.math.shape import Rectangle
from vulk.math.vector import Vector3
from vulk import audio
from vulk import event
from vulk import eventconstant as ec
from vulk import util


ASSET = path.join(path.dirname(path.abspath(__file__)), 'asset')
ASSET_IMAGE = path.join(ASSET, 'images')
ASSET_SOUND = path.join(ASSET, 'sounds')
ASSET_SHADER = path.join(ASSET, 'shaders')


def asset_image(name):
    return path.join(ASSET_IMAGE, name)


def asset_sound(name):
    return path.join(ASSET_SOUND, name)


def asset_shader(name):
    return path.join(ASSET_SHADER, name)


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()

        # Load images
        self.drop_image = Texture(self.context, asset_image('droplet.png'))
        self.bucket_image = Texture(self.context, asset_image('bucket.png'))

        # Load sounds
        self.drop_sound = audio.Sound(asset_sound('drop.wav'))
        self.rain_music = audio.Music(asset_sound('rain.mp3'))

        # Start immediatly background music
        #self.rain_music.play(repeat=0)

        # Initialize camera and spritebatch
        self.camera = OrthographicCamera(800, 480)
        self.camera.update()
        self.spritebatch = SpriteBatch(self.context)

        # Misc parameters
        self.bucket = Rectangle(800 / 2 - 64 / 2, 480 - 20 - 64, 64, 64)
        self.raindrops = []
        self.last_droptime = 0

        # Event managing
        self.delta = 0

        def mouse_drag(x, y, xr, yr, button):
            pos = Vector3([x, y, 0])
            self.camera.unproject(pos, 0, 0, self.context.width,
                                  self.context.height)
            self.bucket.x = pos.x - 62 / 2

        def key_down(keycode):
            if keycode == ec.KeyCode.LEFT:
                self.bucket.x -= 4 * self.delta
            if keycode == ec.KeyCode.RIGHT:
                self.bucket.x += 4 * self.delta

            if self.bucket.x < 0:
                self.bucket.x = 0
            if self.bucket.x > 800 - 64:
                self.bucket.x = 800 - 64

        # Register event listener
        cb = event.CallbackEventListener(
            mouse_drag=mouse_drag, key_down=key_down)
        self.event_listeners.append(cb)

    def spawn_raindrop(self):
        raindrop = Rectangle(random.randrange(0, 800-64), -64, 64, 64)
        self.raindrops.append(raindrop)
        self.last_droptime = util.nanos()

    def update_raindrops(self, delta):
        new_raindrops = []
        for raindrop in self.raindrops:
            raindrop.y += delta / 5
            if raindrop.overlaps(self.bucket):
                pass
                # self.drop_sound.play()
            else:
                new_raindrops.append(raindrop)

        self.raindrops = new_raindrops

    def end(self):
        pass

    def resize(self):
        super().resize()
        self.spritebatch.reload(self.context)

    def render(self, delta):
        self.delta = delta
        if util.nanos() - self.last_droptime > 1000000000:
            self.spawn_raindrop()

        # Clear screen
        self.context.clear_final_image([0, 0, 0.2, 1])

        # Update camera
        self.camera.update()

        # Move raindrop
        self.update_raindrops(delta)

        # Render with sprtebatch
        self.spritebatch.update_projection(self.camera.combined)
        self.spritebatch.begin(self.context)
        self.spritebatch.draw(self.bucket_image, self.bucket.x, self.bucket.y)

        for raindrop in self.raindrops:
            self.spritebatch.draw(self.drop_image, raindrop.x, raindrop.y)

        spritebatch_semaphore = self.spritebatch.end()

        self.context.swap([spritebatch_semaphore])


def main():
    app = App(debug=True)
    with app as a:
        a.run()


if __name__ == "__main__":
    main()
