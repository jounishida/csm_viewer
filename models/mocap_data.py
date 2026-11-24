import os
import numpy as np


class MocapData:

    def __init__(self):

        self.frames = None
        self.points = None

        self.n_frames = 0
        self.n_points = 0

        self.filename = ""

    def clear(self):

        self.frames = None
        self.points = None

        self.n_frames = 0
        self.n_points = 0

        self.filename = ""

    def is_loaded(self):

        return self.points is not None

    def load_file(self, filename):

        rows = []

        with open(
            filename,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            for line in f:

                parts = line.split()

                if (
                    len(parts) > 0
                    and
                    parts[0].isdigit()
                ):
                    rows.append(
                        [float(v) for v in parts]
                    )

        if not rows:
            raise RuntimeError(
                "Nenhum frame encontrado."
            )

        data = np.asarray(rows)

        self.frames = data[:, 0].astype(int)

        self.points = data[:, 1:].reshape(
            len(data),
            -1,
            3
        )

        self.n_frames = (
            self.points.shape[0]
        )

        self.n_points = (
            self.points.shape[1]
        )

        self.filename = (
            os.path.basename(filename)
        )

    def global_bounds(self):

        mins = self.points.min(
            axis=(0, 1)
        )

        maxs = self.points.max(
            axis=(0, 1)
        )

        return mins, maxs

    def frame_bounds(self, frame):

        xyz = self.points[frame]

        mins = xyz.min(axis=0)

        maxs = xyz.max(axis=0)

        return mins, maxs

    def get_frame(self, frame):

        return self.points[frame]
