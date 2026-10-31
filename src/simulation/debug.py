import pyglet
from pyglet import text, graphics

from src.config import get_config

__all__ = ["DebugManager"]

_config = get_config('debug')
_label_data = {
    "font_size": _config["font_size"], "font_name": _config["font_name"],
    "color": _config["font_color"],
    "x": _config["font_spacing"],
}


class DebugManager:
    def __init__(self, window_size: tuple[int, int]) -> None:
        self._active = False

        self.batch = graphics.Batch()

        self._labels = {
            "fps": text.Label(
                "fps: 0", y = (window_size[1] - (_config["font_size"] + _config["font_spacing"])), batch=self.batch,
                **_label_data
            ),
        }

        self._time_set = []

    def change_active(self) -> None:
        self._active = not self._active

    def update_stats(self, delta: float) -> None:
        times = self._time_set

        if len(times) >= 30:
            times.pop(0)
        times.append(delta)

        if sum(times) == 0:
            framerate = 0
        else:
            framerate = round(len(times) / sum(times), 1)
        self._labels["fps"].text = f"fps: {framerate}"

    def update_position(self, window_size: tuple[int, int]) -> None:
        for i, label in enumerate(self._labels.values()):
            label.position = (
                _config["font_spacing"],
                (window_size[1] - (_config["font_size"] + _config["font_spacing"]) * (i + 1)),
                0
            )

    def render(self) -> None:
        if self._active:
            self.batch.draw()
