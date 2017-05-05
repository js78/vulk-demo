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
        data = FontData(self.context, path)
        data2 = FontDataTest(self.context, path)
        data3 = FontDataUgly(self.context, path)
        self.renderer = TextRenderer(self.context, data)
        self.renderer2 = TextRenderer(self.context, data2)
        self.renderer3 = TextRenderer(self.context, data3)

    def end(self):
        pass

    def reload(self):
        pass

    def render(self, delta):
        # Clear screen
        self.context.clear_final_image([0, 0, 0.2, 1])

        self.renderer.begin(self.context)
        self.renderer.draw("I am a test", 10, 10, 30)
        self.renderer.draw("I am a test", 10, 100, 40)
        self.renderer.draw("I am a test", 10, 200, 20)
        self.renderer.draw("I am a test", 10, 300, 10)
        sem1 = self.renderer.end()

        self.renderer2.begin(self.context)
        self.renderer2.draw("I am a test", 200, 10, 30)
        self.renderer2.draw("I am a test", 200, 100, 40)
        self.renderer2.draw("I am a test", 200, 200, 20)
        self.renderer2.draw("I am a test", 200, 300, 10)
        sem2 = self.renderer2.end()

        self.renderer3.begin(self.context)
        self.renderer3.draw("I am a test", 400, 10, 30)
        self.renderer3.draw("I am a test", 400, 100, 40)
        self.renderer3.draw("I am a test", 400, 200, 20)
        self.renderer3.draw("I am a test", 400, 300, 10)
        sem3 = self.renderer3.end()

        self.context.swap([sem1, sem2, sem3])


def main():
    app = App(debug=True)
    with app as a:
        a.run()


if __name__ == "__main__":
    main()
