#!/usr/bin/env python3.6
from os import path

from vulk.baseapp import BaseApp
from vulk.graphic.texture import Texture
from vulk.graphic.d2.spritebatch import SpriteBatch


ASSET = path.join(path.dirname(path.abspath(__file__)), 'asset')
ASSET_IMAGE = path.join(ASSET, 'images')


def asset_image(name):
    return path.join(ASSET_IMAGE, name)


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()

        self.vulkan_image = Texture(self.context, asset_image('vulkan.png'))
        self.bucket_image = Texture(self.context, asset_image('bucket.png'))
        self.spritebatch = SpriteBatch(self.context)
        self.a = 1
        self.fadeout = True
        self.rotation = 0

        print("You must see 2 vulkan images and 1 bucket image")

    def end(self):
        pass

    def reload(self):
        pass

    def render(self, delta):
        # Clear screen
        self.context.clear_final_image([0, 0, 0.2, 1])

        # Render with sprtebatch
        self.spritebatch.begin(self.context)
        self.spritebatch.draw(self.vulkan_image, 0, 0)
        self.spritebatch.draw(self.vulkan_image, 50, 50, a=self.a)
        self.spritebatch.draw(self.bucket_image, 70, 70,
                              rotation=self.rotation, scale_x=2, scale_y=0.5)
        spritebatch_semaphore = self.spritebatch.end()
        self.context.swap([spritebatch_semaphore])

        speed = 0.01
        self.rotation += speed * 1 / delta
        if self.fadeout:
            self.a -= speed * 1 / delta
            if self.a <= 0:
                self.fadeout = False
        else:
            self.a += speed * 1 / delta
            if self.a >= 1:
                self.fadeout = True


def main():
    app = App(debug=True)
    with app as a:
        a.run()


if __name__ == "__main__":
    main()
