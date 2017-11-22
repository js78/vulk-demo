#!/usr/bin/env python3.6
from os import path

from vulk.baseapp import BaseApp
from vulk.graphic.camera import OrthographicCamera
from vulk.graphic.texture import Texture, TextureRegion
from vulk.graphic.d2.ui import Ui
from vulk.math import interpolation
from vulk.graphic.d2.font import FontData


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
        self.ui = Ui(self.context, "html_file.html")

    def end(self):
        pass

    def resize(self):
        super().resize()
        self.ui.resize(self.context)

    def render(self, delta):
        self.context.clear_final_image([0, 0, 0.2, 1])
        sem = self.ui.render(self.context)
        self.context.swap([sem] if sem else [])


def main():
    app = App(debug=True)
    with app as a:
        a.run()


if __name__ == "__main__":
    main()
