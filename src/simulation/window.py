import pyglet

from src import __title__, __version__
from src.config import get_config
from .rendering import Renderer

__all__ = ["Window"]

_config = get_config('window')


class Window:
    def __init__(self) -> None:
        self.window = pyglet.window.Window(
            caption = f"{__title__}  |  v{__version__}",
            width = _config['width'], height = _config['height'],
            resizable = _config['resizable']
        )
        self.window.push_handlers(self)

        self.renderer = Renderer(self.window)

    def on_update(self, delta: float) -> None:
        pass

    def on_draw(self) -> None:
        self.window.clear()
        self.renderer.render()

    def run(self) -> None:
        pyglet.clock.schedule_interval(self.on_update, 1/60)
        pyglet.app.run()
