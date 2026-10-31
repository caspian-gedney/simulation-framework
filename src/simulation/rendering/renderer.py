from pyglet import image, window
from pyglet.gl import *
from pyglet.math import Mat4

from src.config import get_config
from .shaders import ShaderManager

__all__ = ["Renderer"]

_config = get_config('simulation')


class Renderer:
    def __init__(self, sim_window: window.Window) -> None:
        self._window = sim_window

        self._create_render_target()
        self._load_shader()
        self._create_quad()

    def _create_render_target(self) -> None:
        self.virtual_tex = image.Texture.create(
            _config["width"], _config["height"]
        )

        self.framebuffer = image.Framebuffer()
        self.framebuffer.attach_texture(self.virtual_tex)

    def _load_shader(self) -> None:
        self.shaders = ShaderManager()
        self.shaders.add("scale")
        self.program = self.shaders.get("scale")

    def _create_quad(self) -> None:
        self.quad = self.program.vertex_list(
            4,
            GL_TRIANGLE_STRIP,
            position=("f2", [-1, -1, 1, -1, -1, 1, 1, 1]),
            texcoord=("f2", [0, 0, 1, 0, 0, 1, 1, 1]),
        )

    def _draw_scene(self) -> None:
        pass

    def compute_letterbox(self) -> tuple[int, int, int, int]:
        iw, ih = _config["width"], _config["height"]
        ew, eh = self._window.get_size()

        scale = min(ew / iw, eh / ih)
        new_w = int(iw * scale)
        new_h = int(ih * scale)

        x = (ew - new_w) // 2
        y = (eh - new_h) // 2

        return x, y, new_w, new_h

    @staticmethod
    def _clear(width: int, height: int, color: list[float]) -> None:
        glViewport(0, 0, width, height)
        glClearColor(*color, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def _render_to_texture(self) -> None:
        self.framebuffer.bind()

        self._clear(
            _config["width"], _config["height"],
            _config["background_color"]
        )

        self._window.projection = Mat4.orthogonal_projection(
            0, _config["width"],
            0, _config["height"],
            -1, 1
        )

        self._draw_scene()
        self.framebuffer.unbind()

    def _bind_virtual_texture(self) -> None:
        glActiveTexture(GL_TEXTURE0)
        self.virtual_tex.bind()

        self.program.use()
        self.program["screen_tex"] = 0

    def _render_to_screen(self) -> None:
        x, y, new_w, new_h = self.compute_letterbox()

        width, height = self._window.get_size()
        self._clear(
            width, height,
            _config["letterbox_color"]
        )

        glViewport(x, y, new_w, new_h)

        self._bind_virtual_texture()

        self.quad.draw(GL_TRIANGLE_STRIP)

        glViewport(0, 0, width, height)
        self._window.projection = Mat4.orthogonal_projection(
            0, width, 0, height, -1, 1
        )

    def render(self):
        self._render_to_texture()
        self._render_to_screen()
