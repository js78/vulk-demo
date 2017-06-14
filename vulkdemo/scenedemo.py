#!/usr/bin/env python3.6
from os import path

from vulk.baseapp import BaseApp
from vulk.graphic.camera import OrthographicCamera
from vulk.graphic.texture import Texture, TextureRegion
from vulk.graphic.d2 import scene
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

        path = '/home/realitix/git/vulk/vulk/asset/font/arial.fnt'
        fontdata = FontData(self.context, path)
        camera = OrthographicCamera(self.context.width, self.context.height)
        self.viewport = scene.ScreenViewport(camera)
        self.viewport.update(self.context.width, self.context.height)
        self.scene = scene.BatchedScene(self.context, self.viewport)
        region = TextureRegion(Texture(self.context,
                                       asset_image('vulkan.png')))

        #container = scene.Widget(self.scene)
        #container.place(width=self.context.width, height=100, x=0, y=0)

        widget0 = scene.Image(self.scene, region)
        widget0.grid(column=0, row=0)
        widget1 = scene.Block(self.scene)
        widget1.color = [0,0,1,1]
        widget1.grid(column=1, row=0)

        #widget1 = scene.Image(self.scene, region)
        #widget1.grid(column=1, row=0)

        #widget2 = scene.Image(widget1, region)
        #widget2.grid(column=0, row=0)

        #widget3 = scene.Image(widget1, region)
        #widget3.grid(column=0, row=1)

        #widget4 = scene.Image(widget3, region)
        #widget4.grid(column=0, row=0)

        #widget5 = scene.Image(widget3, region)
        #widget5.grid(column=1, row=0)


        #widget7 = scene.Image(self.scene, region)
        #widget7.place(width=60, height=60, x=100, y=100)
        #action1 = scene.MoveBy(x=300, y=0, duration=3000, interpolation=interpolation.Smooth())
        action1 = scene.MoveBy(x=100, y=0, duration=1000, interpolation=interpolation.Smooth())
        action2 = scene.MoveBy(x=0, y=100, duration=3000)
        parallel = scene.Parallel([action1, action2])
        repeat = scene.Repeat(parallel)
        #action1 = scene.MoveTo(x=400, y=100, duration=3000, interpolation=interpolation.Smooth())
        #action2 = scene.MoveBy(x=0, y=100, duration=3000)
        #action3 = scene.FadeTo(fade=0.5, duration=1000)
        #widget7.add_action(scene.Sequence([action1, action2, action3]))
        def get_parallel():
            s = interpolation.Smooth()
            fadein = scene.FadeIn(500, s)
            fadeout = scene.FadeOut(500, s)
            sequence = scene.Sequence([fadein, fadeout])
            repeat_fade = scene.Repeat(sequence)

            m = scene.MoveBy
            repeat_move = scene.Repeat(scene.Sequence([
                m(100, 0, 500, s), m(0, 100, 500, s), m(-100, -100, 1000, s)]))

            return [repeat_fade, repeat_move]

        #widget7.add_action(scene.Parallel(get_parallel()))

        #widget6 = scene.Block(self.scene)
        #widget6.place(width=200, height=200, x=300, y=300)
        #widget6.add_action(scene.Parallel(get_parallel()))

        #widget9 = scene.Block(self.scene)
        #widget9.place(width=1, height=200, x=300, y=300)
        #widget9.add_action(scene.RotateTo(-1, 1000))

        widget10 = scene.Label(self.scene, fontdata, 'arial')
        widget10.color[:] = [1., 0., 0., 1.]
        widget10.place(width=150, height=150, x=300, y=100)

        #widget10.add_action(scene.RotateBy(50, 200000))

    def end(self):
        pass

    def resize(self):
        super().resize()
        self.scene.resize(self.context)

    def render(self, delta):
        self.context.clear_final_image([0, 0, 0.2, 1])
        self.scene.update(delta)
        sem = self.scene.render(self.context)
        self.context.swap([sem] if sem else [])


def main():
    app = App(debug=True)
    with app as a:
        a.run()


if __name__ == "__main__":
    main()
