import pyglet

from src import __title__, __version__
from src.config import get_config
from .debug import DebugManager
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

        self.debug = DebugManager(self.window.get_size())
        self.renderer = Renderer(self.window)

    def on_resize(self, width: int, height: int) -> None:
        self.debug.update_position((width, height))

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == pyglet.window.key.F3:
            self.debug.change_active()

    def on_update(self, delta: float) -> None:
        self.debug.update_stats(delta)

    def on_draw(self) -> None:
        self.window.clear()
        self.renderer.render()
        self.debug.render()

    def run(self) -> None:
        pyglet.clock.schedule_interval(self.on_update, 1/_config['framerate'])
        pyglet.app.run()
