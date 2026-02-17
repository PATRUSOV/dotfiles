from dataclasses import dataclass
from typing import Self, Sequence


@dataclass(frozen=True)
class HyprlandMonitor:
    name: str
    resolution: str
    update_rate: int
    position: str
    scale: int
    disabled: bool = False

    def __str__(self) -> str:
        if self.disabled:
            return f"{self.name}, disable"
        return f"{self.name}, {self.resolution}@{self.update_rate}, {self.position}, {self.scale}"

    @classmethod
    def make_disabled(cls, name: str) -> Self:
        monitor = cls(name, "0x0", 0, "0x0", 1, True)
        return monitor


class HyprlandMonitorsConfiguration:
    def __init__(self, name: str, monitors: Sequence[HyprlandMonitor]) -> None:
        self.name = name
        self.monitors = monitors

    def __str__(self) -> str:
        description = f"# configuration: {self.name}\n\n"
        monitors_dumps = "\n".join(f"monitor = {monitor}" for monitor in self.monitors)

        return description + monitors_dumps
