from pyglet.graphics.shader import Shader, ShaderProgram

from src import ROOT_PATH

__all__ = ["ShaderManager"]


class ShaderManager:
    def __init__(self) -> None:
        self._programs: dict[str, ShaderProgram]  = {}

    @staticmethod
    def _load_source(name: str) -> tuple[str, str]:
        vert_path = ROOT_PATH / f"assets/shaders/{name}.vert"
        frag_path = ROOT_PATH / f"assets/shaders/{name}.frag"

        if not vert_path.is_file() or not frag_path.is_file():
            raise FileNotFoundError(f"Failed to load shader {name}")

        vert_str = vert_path.read_text(encoding="utf-8")
        frag_str = frag_path.read_text(encoding="utf-8")

        return vert_str, frag_str

    def add(self, name:str) -> None:
        vert_src, frag_src = self._load_source(name)

        vert_shader = Shader(vert_src, "vertex")
        frag_shader = Shader(frag_src, "fragment")

        program = ShaderProgram(vert_shader, frag_shader)
        self._programs[name] = program

    def get(self, name: str) -> ShaderProgram:
        if name not in self._programs:
            raise KeyError(f"Shader {name} not found")

        return self._programs[name]
