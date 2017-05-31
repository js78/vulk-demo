#!/usr/bin/env python3.6
from vulk.baseapp import BaseApp
from vulk.graphic.d2.batch import BlockBatch, BlockProperty


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()

        self.batch = BlockBatch(self.context)
        self.properties = BlockProperty()
        self.properties.x = 200
        self.properties.y = 200
        self.properties.width = 200
        self.properties.height = 200

        # colors
        self.properties.colors[0] = [0., 1., 0., 1.]
        self.properties.colors[1] = [1., 0., 0., 1.]
        self.properties.colors[2] = [0., 0., 1., 1.]
        self.properties.colors[3] = [1., 1., 1., 1.]

        # border top
        self.properties.border_colors[0] = [1., 0., 0., 1.]
        self.properties.border_widths[0] = 0.1
        # border right
        self.properties.border_colors[1] = [0., 1., 0., 1.]
        self.properties.border_widths[1] = 0.05
        # border bottom
        self.properties.border_colors[2] = [0., 0., 1., 1.]
        self.properties.border_widths[2] = 0.03
        # border left
        self.properties.border_colors[3] = [1., 0., 1., 1.]
        self.properties.border_widths[3] = 0.01

    def end(self):
        pass

    def reload(self):
        pass

    def resize(self):
        super().resize()
        self.batch.resize(self.context)

    def render(self, delta):
        # Clear screen
        self.context.clear_final_image([0, 0, 0.2, 1])

        # Rotation
        self.properties.rotation += delta * 0.001
        self.properties.rotation %= 360
        self.properties.border_radius[0] += 0.0002 * delta
        self.properties.border_radius[1] += 0.0002 * delta
        self.properties.border_radius[2] += 0.0002 * delta
        self.properties.border_radius[3] += 0.0002 * delta

        # Render with batch
        self.batch.begin(self.context)
        self.batch.draw(self.properties)
        batch_semaphore = self.batch.end()
        self.context.swap([batch_semaphore])


def main():
    app = App(debug=True)
    with app as a:
        a.run()


if __name__ == "__main__":
    main()
