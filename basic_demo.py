from vulk.container.desktopcontainer import DesktopContainer
from vulk.baseapp import BaseApp
from vulk.graphic.mesh import Mesh

import OpenGL.GL as gl

vertex_shader = """
#version 330

in vec2 position;

void main() {
    gl_Position = vec4(position.x, position.y, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330

out vec4 frag

void main() {
    frag = vec4(1.0, 0.0, 0.0, 1.0);
}
"""


class TestApp(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mesh = Mesh(self.driver, 3, {'position': 2})
        self.shaderprogram = self.driver.shader_program(vertex_shader,
                                                        fragment_shader)

        vertices = [-0.5, -0.5,
                    0.5, -0.5,
                    0.5, 0.5]
        self.mesh.bind_shader(self.shaderprogram._shader_program)
        self.mesh.vertices = vertices

    def render(self):
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        with self.shaderprogram:
            with self.mesh:
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

test = DesktopContainer(TestApp)
test.run()
