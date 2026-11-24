import numpy as np


class CameraController:

    def __init__(self):

        self.center = np.array(
            [0.0, 0.0, 0.0],
            dtype=float
        )

        self.radius = 100.0

        self.default_radius = 100.0

        self.elev = 30.0
        self.azim = 45.0
        self.roll = 0.0

    # ==========================================
    # ENQUADRAMENTO
    # ==========================================

    def fit_box(
        self,
        mins,
        maxs,
        margin_percent=20.0
    ):

        self.center = (
            mins + maxs
        ) / 2.0

        size = np.max(
            maxs - mins
        )

        margin = (
            float(margin_percent)
            / 100.0
        )

        self.radius = (
            size * (0.5 + margin)
        )

        self.default_radius = (
            self.radius
        )

    # ==========================================
    # LIMITES
    # ==========================================

    def apply(self, ax):

        cx, cy, cz = self.center

        r = self.radius

        ax.set_xlim(
            cx - r,
            cx + r
        )

        ax.set_ylim(
            cy - r,
            cy + r
        )

        ax.set_zlim(
            cz - r,
            cz + r
        )

        try:

            ax.view_init(
                elev=self.elev,
                azim=self.azim,
                roll=self.roll
            )

        except TypeError:

            ax.view_init(
                elev=self.elev,
                azim=self.azim
            )

    # ==========================================
    # ZOOM
    # ==========================================

    def zoom(self, factor):

        self.radius *= factor

        self.radius = max(
            self.radius,
            1e-3
        )

    def reset_zoom(self):

        self.radius = (
            self.default_radius
        )

    # ==========================================
    # ORIENTACAO
    # ==========================================

    def reset_orientation(self):

        self.elev = 30.0

        self.azim = 45.0

        self.roll = 0.0

    def rotate(
        self,
        dx,
        dy
    ):

        self.azim += dx * 0.5

        self.elev -= dy * 0.5

    def rotate_x(
        self,
        angle
    ):

        self.elev += angle

    def rotate_y(
        self,
        angle
    ):

        self.azim += angle

    def rotate_z(
        self,
        angle
    ):

        self.roll += angle

    # ==========================================
    # PAN
    # ==========================================

    def pan(
        self,
        dx,
        dy
    ):

        az = np.radians(
            self.azim
        )

        el = np.radians(
            self.elev
        )

        forward = np.array(
            [
                np.cos(el) * np.cos(az),
                np.cos(el) * np.sin(az),
                np.sin(el)
            ]
        )

        world_up = np.array(
            [0.0, 0.0, 1.0]
        )

        right = np.cross(
            forward,
            world_up
        )

        nr = np.linalg.norm(
            right
        )

        if nr > 1e-8:
            right /= nr
        else:
            right = np.array(
                [1.0, 0.0, 0.0]
            )

        up = np.cross(
            right,
            forward
        )

        scale = (
            self.radius
            * 0.002
        )

        displacement = (
            (-dx * right)
            + (dy * up)
        ) * scale

        self.center += displacement

    # ==========================================
    # ESTADO
    # ===================================
