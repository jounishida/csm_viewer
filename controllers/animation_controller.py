from PyQt5.QtCore import (
    QTimer
)


class AnimationController:

    def __init__(
        self,
        callback
    ):

        self.timer = QTimer()

        self.timer.timeout.connect(
            callback
        )

    def start(
        self,
        fps
    ):

        fps = max(
            1,
            int(fps)
        )

        self.timer.start(
            int(1000 / fps)
        )

    def stop(self):

        self.timer.stop()

    def is_running(self):

        return (
            self.timer.isActive()
        )
