from __future__ import annotations

from abc import ABC, abstractmethod

from config import PlotterConfig
from motion import MotionCommand, PenState


class PlotterDriver(ABC):
    # Shared interface for anything that can execute motion commands.
    # Today this is a mock driver; real hardware should implement this same shape.
    @abstractmethod
    def home(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def pen_up(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def pen_down(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def move_to(self, x_mm: float, y_mm: float, feed_rate_mm_min: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        raise NotImplementedError


class MockPlotterDriver(PlotterDriver):
    # PC-safe driver that prints each move instead of touching hardware.
    # Useful for checking the workflow before the Jetson and CNC controller exist.
    def __init__(self, config: PlotterConfig) -> None:
        self.config = config
        self.x_mm = config.home_x_mm
        self.y_mm = config.home_y_mm
        self.pen = PenState.UP

    def home(self) -> None:
        self.x_mm = self.config.home_x_mm
        self.y_mm = self.config.home_y_mm
        print(f"HOME -> x={self.x_mm:.2f}, y={self.y_mm:.2f}")

    def pen_up(self) -> None:
        if self.pen != PenState.UP:
            print(f"PEN UP -> servo angle {self.config.pen_up_angle}")
        self.pen = PenState.UP

    def pen_down(self) -> None:
        if self.pen != PenState.DOWN:
            print(f"PEN DOWN -> servo angle {self.config.pen_down_angle}")
        self.pen = PenState.DOWN

    def move_to(self, x_mm: float, y_mm: float, feed_rate_mm_min: float) -> None:
        self.x_mm = x_mm
        self.y_mm = y_mm
        print(f"MOVE -> x={x_mm:.2f}, y={y_mm:.2f}, feed={feed_rate_mm_min:.1f} mm/min")

    def shutdown(self) -> None:
        self.pen_up()
        print("SHUTDOWN")


class JetsonPlotterDriver(PlotterDriver):
    # Placeholder for a direct hardware driver.
    # The current plan favors GRBL on an Arduino Uno, so this may remain unused.
    def __init__(self, config: PlotterConfig) -> None:
        self.config = config
        raise NotImplementedError("Jetson GPIO stepper and servo control will be added after hardware setup.")

    def home(self) -> None:
        raise NotImplementedError

    def pen_up(self) -> None:
        raise NotImplementedError

    def pen_down(self) -> None:
        raise NotImplementedError

    def move_to(self, x_mm: float, y_mm: float, feed_rate_mm_min: float) -> None:
        raise NotImplementedError

    def shutdown(self) -> None:
        raise NotImplementedError


def run_commands(driver: PlotterDriver, commands: list[MotionCommand]) -> None:
    # Execute the high-level command list through any driver implementation.
    # This is separate from G-code export so mock testing remains easy.
    driver.home()

    for command in commands:
        if command.pen == PenState.DOWN:
            driver.pen_down()
        else:
            driver.pen_up()
        driver.move_to(command.x, command.y, command.feed_rate_mm_min)

    driver.shutdown()
