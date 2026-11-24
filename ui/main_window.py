from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QFileDialog,
    QPushButton,
    QLabel,
    QLineEdit,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QMessageBox,
    QStatusBar
)

from PyQt5.QtGui import (
    QDoubleValidator
)

from PyQt5.QtCore import Qt

from ui.canvas_3d import Canvas3D

from controllers.camera_controller import (
    CameraController
)

from controllers.animation_controller import (
    AnimationController
)

from models.mocap_data import (
    MocapData
)

from models.view_manager import (
    ViewManager
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "CSM Viewer"
        )

        self.resize(
            1400,
            900
        )

        self.data = MocapData()

        self.camera = CameraController()

        self.views = ViewManager()

        self.frame_atual = 0

        self.scatter = None

        self.movimento_cache = None

        self.rotacionando = False
        self.movendo = False

        self.last_x = 0
        self.last_y = 0

        self.animation = (
            AnimationController(
                self.avancar_frame
            )
        )

        self.criar_interface()

        self.conectar_mouse()

    # ==================================================
    # UI
    # ==================================================

    def criar_interface(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QVBoxLayout()

        central.setLayout(
            layout
        )

        self.criar_toolbar(
            layout
        )

        self.criar_canvas(
            layout
        )

        self.criar_slider(
            layout
        )

        self.criar_info(
            layout
        )

        self.setStatusBar(
            QStatusBar()
        )

    # ==================================================

    def criar_toolbar(
        self,
        layout
    ):

        topo = QHBoxLayout()

        # --------------------------------

        self.bt_abrir = QPushButton(
            "Abrir"
        )

        topo.addWidget(
            self.bt_abrir
        )

        # --------------------------------

        self.bt_play = QPushButton(
            "Play"
        )

        self.bt_pause = QPushButton(
            "Pause"
        )

        topo.addWidget(
            self.bt_play
        )

        topo.addWidget(
            self.bt_pause
        )

        # --------------------------------

        self.bt_home = QPushButton(
            "Home"
        )

        self.bt_reset_zoom = (
            QPushButton(
                "Reset Zoom"
            )
        )

        self.bt_fit_all = (
            QPushButton(
                "Fit All"
            )
        )

        self.bt_fit_frame = (
            QPushButton(
                "Fit Frame"
            )
        )

        topo.addWidget(
            self.bt_home
        )

        topo.addWidget(
            self.bt_reset_zoom
        )

        topo.addWidget(
            self.bt_fit_all
        )

        topo.addWidget(
            self.bt_fit_frame
        )

        # --------------------------------

        self.bt_xm = QPushButton(
            "X-"
        )

        self.bt_xp = QPushButton(
            "X+"
        )

        self.bt_ym = QPushButton(
            "Y-"
        )

        self.bt_yp = QPushButton(
            "Y+"
        )

        self.bt_zm = QPushButton(
            "Z-"
        )

        self.bt_zp = QPushButton(
            "Z+"
        )

        topo.addWidget(
            self.bt_xm
        )

        topo.addWidget(
            self.bt_xp
        )

        topo.addWidget(
            self.bt_ym
        )

        topo.addWidget(
            self.bt_yp
        )

        topo.addWidget(
            self.bt_zm
        )

        topo.addWidget(
            self.bt_zp
        )

        # --------------------------------

        topo.addWidget(
            QLabel("FPS")
        )

        self.ed_fps = QLineEdit(
            "120"
        )

        self.ed_fps.setFixedWidth(
            60
        )

        topo.addWidget(
            self.ed_fps
        )

        # --------------------------------

        topo.addWidget(
            QLabel("Margem %")
        )

        self.ed_fit_margin = (
            QLineEdit("20")
        )

        self.ed_fit_margin.setFixedWidth(
            70
        )

        self.ed_fit_margin.setValidator(
            QDoubleValidator(
                0.0,
                500.0,
                2
            )
        )

        topo.addWidget(
            self.ed_fit_margin
        )

        # --------------------------------

        self.chk_estaticos = (
            QCheckBox(
                "Ocultar estáticos"
            )
        )

        topo.addWidget(
            self.chk_estaticos
        )

        topo.addWidget(
            QLabel("Frames")
        )

        self.ed_frames = QLineEdit(
            "5"
        )

        self.ed_frames.setFixedWidth(
            50
        )

        topo.addWidget(
            self.ed_frames
        )

        topo.addWidget(
            QLabel("Tol")
        )

        self.ed_tol = QLineEdit(
            "1.0"
        )

        self.ed_tol.setFixedWidth(
            60
        )

        topo.addWidget(
            self.ed_tol
        )

        topo.addStretch()

        layout.addLayout(
            topo
        )

    # ==================================================

    def criar_canvas(
        self,
        layout
    ):

        self.canvas = Canvas3D()

        self.canvas.prepare_scene()

        layout.addWidget(
            self.canvas
        )

    # ==================================================

    def criar_slider(
        self,
        layout
    ):

        self.slider = QSlider(
            Qt.Horizontal
        )

        self.slider.setMinimum(
            0
        )

        layout.addWidget(
            self.slider
        )

    # ==================================================

    def criar_info(
        self,
        layout
    ):

        self.lbl_info = QLabel(
            "Nenhum arquivo carregado"
        )

        layout.addWidget(
            self.lbl_info
        )
