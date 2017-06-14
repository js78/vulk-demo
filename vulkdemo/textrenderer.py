#!/usr/bin/env python3.6
from vulk.baseapp import BaseApp
from vulk.graphic.d2.font import FontData, TextRenderer
from vulk.graphic.texture import Texture


class FontDataTest(FontData):
    def _init_pages(self, context):
        res = {}
        dirpath = self.filepath.parent
        for p in self.raw_data['page']:
            res[p['id']] = Texture(context, dirpath / p['file'], mip_levels=0)

        return res


class FontDataUgly(FontData):
    def _init_pages(self, context):
        res = {}
        dirpath = self.filepath.parent
        for p in self.raw_data['page']:
            res[p['id']] = Texture(context, dirpath / p['file'])

        return res


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()
        path = '/home/realitix/git/vulk/vulk/asset/font/arial.fnt'
        self.data = FontData(self.context, path)
        self.data2 = FontDataTest(self.context, path)
        self.data3 = FontDataUgly(self.context, path)
        self.renderer = TextRenderer(self.context)

    def end(self):
        pass

    def resize(self):
        super().resize()
        self.renderer.reload(self.context)

    def render(self, delta):
        # Clear screen
        self.context.clear_final_image([0, 0, 0.2, 1])

        self.renderer.begin(self.context)
        self.renderer.draw(self.data, "I am a test", 10, 10, 30)
        self.renderer.draw(self.data, "I am a test", 10, 100, 40)
        self.renderer.draw(self.data, "I am a test", 10, 200, 20)
        self.renderer.draw(self.data, "I am a test", 10, 300, 10)

        self.renderer.draw(self.data2, "I am a test", 200, 10, 30)
        self.renderer.draw(self.data2, "I am a test", 200, 100, 40)
        self.renderer.draw(self.data2, "I am a test", 200, 200, 20)
        self.renderer.draw(self.data2, "I am a test", 200, 300, 10)

        self.renderer.draw(self.data3, "I am a test", 400, 10, 30)
        self.renderer.draw(self.data3, "I am a test", 400, 100, 40)
        self.renderer.draw(self.data3, "I am a test", 400, 200, 20)
        self.renderer.draw(self.data3, "I am a test", 400, 300, 10)
        sem = self.renderer.end()

        self.context.swap([sem])


def main():
    app = App(debug=True)
    with app as a:
        a.run()


if __name__ == "__main__":
    main()
