#!/usr/bin/env python3.6
from vulk.baseapp import BaseApp
from vulk.graphic.d2.font import FontData, TextRenderer


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()
        data = FontData(self.context, '/home/realitix/git/vulk/vulk/asset/font/arial.fnt')
        self.renderer = TextRenderer(self.context, data)


    def end(self):
        pass

    def reload(self):
        pass

    def render(self, delta):
        # Clear screen
        self.context.clear_final_image([0, 0, 0.2, 1])

        self.renderer.begin(self.context)
        self.renderer.draw("I am a test", 10, 10, 30)
        batch_semaphore = self.renderer.end()
        self.context.swap([batch_semaphore])


def main():
    app = App(debug=True)
    with app as a:
        a.run()


if __name__ == "__main__":
    main()
