from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg
)


class Canvas3D(
    FigureCanvasQTAgg
):

    def __init__(self):

        self.fig = Figure(
            figsize=(10, 8)
        )

        self.ax = self.fig.add_subplot(
            111,
            projection="3d"
        )

        super().__init__(
            self.fig
        )

    def prepare_scene(self):

        self.ax.grid(False)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])

        try:

            self.ax.xaxis.pane.fill = False
            self.ax.yaxis.pane.fill = False
            self.ax.zaxis.pane.fill = False

        except:

            pass

    def create_scatter(self):

        self.scatter = (
            self.ax.scatter(
                [],
                [],
                [],
                s=8,
                cmap="viridis"
            )
        )

        return self.scatter
