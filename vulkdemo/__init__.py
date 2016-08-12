from vulk.graphic import constant
from vulk.baseapp import BaseApp
from vulk.graphic.mesh import Mesh

vertex_shader = """
#version 330

in vec2 position;

void main() {
    gl_Position = vec4(position.x, position.y, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330

out vec4 frag;

void main() {
    frag = vec4(1.0, 1.0, 1.0, 1.0);
}
"""


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mesh = Mesh(self.driver, 3, 3, {'position': 2})
        self.shaderprogram = self.driver.shader_program(vertex_shader,
                                                        fragment_shader)

        vertices = [-0.5, -0.5,
                    0.5, -0.5,
                    0.5, 0.5]
        indices = [0, 1, 2]
        self.mesh.bind_attributes(self.shaderprogram)
        self.mesh.vertices = vertices
        self.mesh.indices = indices

    def render(self, delta):
        self.driver.clear((0, 0, 0, 1), 1)
        with self.shaderprogram:
            self.mesh.render(constant.TRIANGLES, 0, 3)
