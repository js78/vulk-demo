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

out vec4 frag;

void main() {
    frag = vec4(1.0, 1.0, 1.0, 1.0);
}
"""


class TestApp(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mesh = Mesh(self.driver, 3, 3, {'position': 2})
        self.shaderprogram = self.driver.shader_program(vertex_shader,
                                                        fragment_shader)

        vertices = [-1, -1,
                    1, -1,
                    1, 1]
        indices = [0, 1, 2]
        self.mesh.bind_shader(self.shaderprogram)
        self.mesh.vertices = vertices
        self.mesh.indices = indices

    def render(self):
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.driver.clear((0, 0, 0, 1))
        with self.shaderprogram:
            with self.mesh:
                gl.glDrawElements(gl.GL_TRIANGLES, 3, gl.GL_UNSIGNED_SHORT,
                                  None)

test = DesktopContainer(TestApp)
test.run()
