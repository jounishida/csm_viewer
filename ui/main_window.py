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

import numpy as np

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

    ROTATION_STEP = 10

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

        self.conectar_botoes()

        self.conectar_mouse()

    # ==================================================
    # INTERFACE
    # ==================================================

    def criar_interface(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        self.layout_principal = (
            QVBoxLayout()
        )

        central.setLayout(
            self.layout_principal
        )

        self.criar_toolbar()

        self.criar_canvas()

        self.criar_slider()

        self.criar_info()

        self.setStatusBar(
            QStatusBar()
        )

    # ==================================================

    def criar_toolbar(self):

        toolbar = QHBoxLayout()

        self.layout_principal.addLayout(
            toolbar
        )

        # ---------------------------------

        self.bt_abrir = QPushButton(
            "Abrir"
        )

        toolbar.addWidget(
            self.bt_abrir
        )

        # ---------------------------------

        self.bt_play = QPushButton(
            "Play"
        )

        self.bt_pause = QPushButton(
            "Pause"
        )

        toolbar.addWidget(
            self.bt_play
        )

        toolbar.addWidget(
            self.bt_pause
        )

        # ---------------------------------

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

        toolbar.addWidget(
            self.bt_home
        )

        toolbar.addWidget(
            self.bt_reset_zoom
        )

        toolbar.addWidget(
            self.bt_fit_all
        )

        toolbar.addWidget(
            self.bt_fit_frame
        )

        # ---------------------------------

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

        toolbar.addWidget(
            self.bt_xm
        )

        toolbar.addWidget(
            self.bt_xp
        )

        toolbar.addWidget(
            self.bt_ym
        )

        toolbar.addWidget(
            self.bt_yp
        )

        toolbar.addWidget(
            self.bt_zm
        )

        toolbar.addWidget(
            self.bt_zp
        )

        # ---------------------------------

        toolbar.addWidget(
            QLabel("FPS")
        )

        self.ed_fps = QLineEdit(
            "120"
        )

        self.ed_fps.setFixedWidth(
            60
        )

        toolbar.addWidget(
            self.ed_fps
        )

        # ---------------------------------

        toolbar.addWidget(
            QLabel("Margem")
        )

        self.ed_fit_margin = (
            QLineEdit("20")
        )

        self.ed_fit_margin.setFixedWidth(
            60
        )

        self.ed_fit_margin.setValidator(
            QDoubleValidator(
                0.0,
                500.0,
                2
            )
        )

        toolbar.addWidget(
            self.ed_fit_margin
        )

        # ---------------------------------

        self.chk_estaticos = (
            QCheckBox(
                "Ocultar estáticos"
            )
        )

        toolbar.addWidget(
            self.chk_estaticos
        )

        toolbar.addWidget(
            QLabel("Frames")
        )

        self.ed_frames = (
            QLineEdit("5")
        )

        self.ed_frames.setFixedWidth(
            50
        )

        toolbar.addWidget(
            self.ed_frames
        )

        toolbar.addWidget(
            QLabel("Tol")
        )

        self.ed_tol = QLineEdit(
            "1.0"
        )

        self.ed_tol.setFixedWidth(
            60
        )

        toolbar.addWidget(
            self.ed_tol
        )

        toolbar.addStretch()

    # ==================================================

    def criar_canvas(self):

        self.canvas = Canvas3D()

        self.canvas.prepare_scene()

        self.layout_principal.addWidget(
            self.canvas
        )
        # ==================================================
    # SLIDER
    # ==================================================

    def criar_slider(self):

        self.slider = QSlider(
            Qt.Horizontal
        )

        self.slider.setMinimum(0)

        self.layout_principal.addWidget(
            self.slider
        )

    # ==================================================
    # INFO
    # ==================================================

    def criar_info(self):

        self.lbl_info = QLabel(
            "Nenhum arquivo carregado"
        )

        self.layout_principal.addWidget(
            self.lbl_info
        )

    # ==================================================
    # CONEXOES
    # ==================================================

    def conectar_botoes(self):

        self.bt_abrir.clicked.connect(
            self.abrir_arquivo
        )

        self.bt_play.clicked.connect(
            self.play
        )

        self.bt_pause.clicked.connect(
            self.pause
        )

        self.bt_home.clicked.connect(
            self.vista_iso
        )

        self.bt_reset_zoom.clicked.connect(
            self.reset_zoom
        )

        self.bt_fit_all.clicked.connect(
            self.fit_all
        )

        self.bt_fit_frame.clicked.connect(
            self.fit_frame
        )

        self.bt_xm.clicked.connect(
            lambda:
            self.girar_x(
                -self.ROTATION_STEP
            )
        )

        self.bt_xp.clicked.connect(
            lambda:
            self.girar_x(
                self.ROTATION_STEP
            )
        )

        self.bt_ym.clicked.connect(
            lambda:
            self.girar_y(
                -self.ROTATION_STEP
            )
        )

        self.bt_yp.clicked.connect(
            lambda:
            self.girar_y(
                self.ROTATION_STEP
            )
        )

        self.bt_zm.clicked.connect(
            lambda:
            self.girar_z(
                -self.ROTATION_STEP
            )
        )

        self.bt_zp.clicked.connect(
            lambda:
            self.girar_z(
                self.ROTATION_STEP
            )
        )

        self.slider.valueChanged.connect(
            self.frame_manual
        )

    # ==================================================
    # UTIL
    # ==================================================

    def obter_fps(self):

        try:

            return max(
                1,
                int(
                    self.ed_fps.text()
                )
            )

        except:

            return 120

    def obter_margem_fit(self):

        txt = (
            self.ed_fit_margin
            .text()
            .strip()
        )

        if txt == "":
            return 20.0

        valor = float(txt)

        valor = max(
            0.0,
            min(500.0, valor)
        )

        return valor

    # ==================================================
    # ARQUIVO
    # ==================================================

    def abrir_arquivo(self):

        arquivo, _ = (
            QFileDialog.getOpenFileName(
                self,
                "Abrir arquivo",
                "",
                "Motion Capture (*.txt *.csm)"
            )
        )

        if not arquivo:
            return

        try:

            self.data.load_file(
                arquivo
            )

            self.frame_atual = 0

            self.slider.blockSignals(
                True
            )

            self.slider.setMaximum(
                self.data.n_frames - 1
            )

            self.slider.setValue(0)

            self.slider.blockSignals(
                False
            )

            self.criar_scatter()

            self.fit_all()

            self.desenhar()

            self.statusBar().showMessage(
                f"Arquivo carregado: "
                f"{self.data.filename}",
                3000
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # ==================================================
    # SCATTER
    # ==================================================

    def criar_scatter(self):

        self.canvas.ax.clear()

        self.canvas.prepare_scene()

        self.scatter = (
            self.canvas.ax.scatter(
                [],
                [],
                [],
                s=8,
                cmap="viridis"
            )
        )

    # ==================================================
    # CAMERA
    # ==================================================

    def atualizar_camera(self):

        self.camera.apply(
            self.canvas.ax
        )

        self.canvas.draw_idle()

    def fit_all(self):

        if not self.data.is_loaded():
            return

        mins, maxs = (
            self.data.global_bounds()
        )

        self.camera.fit_box(
            mins,
            maxs,
            self.obter_margem_fit()
        )

        self.atualizar_camera()

        self.statusBar().showMessage(
            "Fit All",
            1500
        )

    def fit_frame(self):

        if not self.data.is_loaded():
            return

        mins, maxs = (
            self.data.frame_bounds(
                self.frame_atual
            )
        )

        self.camera.fit_box(
            mins,
            maxs,
            self.obter_margem_fit()
        )

        self.atualizar_camera()

        self.statusBar().showMessage(
            "Fit Frame",
            1500
        )

    def vista_iso(self):

        self.camera.reset_orientation()

        self.atualizar_camera()

    def reset_zoom(self):

        self.camera.reset_zoom()

        self.atualizar_camera()

    def reset_camera(self):

        self.fit_all()

        self.camera.reset_orientation()

        self.atualizar_camera()

    def girar_x(self, ang):

        self.camera.rotate_x(
            ang
        )

        self.atualizar_camera()

    def girar_y(self, ang):

        self.camera.rotate_y(
            ang
        )

        self.atualizar_camera()

    def girar_z(self, ang):

        self.camera.rotate_z(
            ang
        )

        self.atualizar_camera()
        # ==================================================
    # MOUSE
    # ==================================================

    def conectar_mouse(self):

        self.canvas.mpl_connect(
            "button_press_event",
            self.mouse_press
        )

        self.canvas.mpl_connect(
            "button_release_event",
            self.mouse_release
        )

        self.canvas.mpl_connect(
            "motion_notify_event",
            self.mouse_move
        )

        self.canvas.mpl_connect(
            "scroll_event",
            self.mouse_scroll
        )

    def mouse_press(self, event):

        if event.x is None:
            return

        self.last_x = event.x
        self.last_y = event.y

        if event.button == 1:
            self.rotacionando = True

        elif event.button == 2:
            self.movendo = True

    def mouse_release(self, event):

        self.rotacionando = False
        self.movendo = False

    def mouse_move(self, event):

        if event.x is None:
            return

        dx = event.x - self.last_x
        dy = event.y - self.last_y

        if self.rotacionando:

            self.camera.rotate(
                dx,
                dy
            )

            self.atualizar_camera()

        elif self.movendo:

            self.camera.pan(
                dx,
                dy
            )

            self.atualizar_camera()

        self.last_x = event.x
        self.last_y = event.y

    def mouse_scroll(self, event):

        if event.button == "up":

            self.camera.zoom(
                0.90
            )

        else:

            self.camera.zoom(
                1.10
            )

        self.atualizar_camera()

    # ==================================================
    # DESENHO
    # ==================================================

    def obter_pontos_frame(self):

        if not self.data.is_loaded():
            return None

        return self.data.get_frame(
            self.frame_atual
        )

    def desenhar(self):

        if not self.data.is_loaded():
            return

        xyz = self.obter_pontos_frame()

        if xyz is None:
            return

        self.scatter._offsets3d = (
            xyz[:, 0],
            xyz[:, 1],
            xyz[:, 2]
        )

        try:

            self.scatter.set_array(
                xyz[:, 2]
            )

        except:
            pass

        self.lbl_info.setText(
            f"{self.data.filename} | "
            f"Frame {self.frame_atual + 1}"
            f"/{self.data.n_frames} | "
            f"Pontos {self.data.n_points}"
        )

        self.canvas.draw_idle()

    # ==================================================
    # ANIMACAO
    # ==================================================

    def play(self):

        fps = self.obter_fps()

        self.animation.start(
            fps
        )

        self.statusBar().showMessage(
            f"Play ({fps} FPS)",
            1500
        )

    def pause(self):

        self.animation.stop()

        self.statusBar().showMessage(
            "Pause",
            1500
        )

    def avancar_frame(self):

        if not self.data.is_loaded():
            return

        self.frame_atual += 1

        if (
            self.frame_atual
            >= self.data.n_frames
        ):
            self.frame_atual = 0

        self.slider.blockSignals(
            True
        )

        self.slider.setValue(
            self.frame_atual
        )

        self.slider.blockSignals(
            False
        )

        self.desenhar()

    def frame_manual(self, valor):

        if not self.data.is_loaded():
            return

        self.frame_atual = valor

        self.desenhar()

    # ==================================================
    # TECLADO
    # ==================================================

    def keyPressEvent(self, event):

        tecla = event.key()

        mods = event.modifiers()

        # --------------------------
        # HOME
        # --------------------------

        if tecla == Qt.Key_Home:

            self.vista_iso()

            return

        # --------------------------
        # SHIFT + R
        # --------------------------

        if (
            tecla == Qt.Key_R
            and
            mods & Qt.ShiftModifier
        ):

            self.reset_camera()

            return

        # --------------------------
        # R
        # --------------------------

        if tecla == Qt.Key_R:

            self.reset_zoom()

            return

        # --------------------------
        # FIT FRAME
        # --------------------------

        if tecla == Qt.Key_F:

            self.fit_frame()

            return

        # --------------------------
        # FIT ALL
        # --------------------------

        if tecla == Qt.Key_A:

            self.fit_all()

            return

        # --------------------------
        # PLAY / PAUSE
        # --------------------------

        if tecla == Qt.Key_Space:

            if self.animation.is_running():

                self.pause()

            else:

                self.play()

            return
            # ==================================================
    # CACHE DE MOVIMENTO
    # ==================================================

    def recalcular_cache_movimento(self):

        if not self.data.is_loaded():
            return

        try:

            janela = max(
                1,
                int(self.ed_frames.text())
            )

        except:

            janela = 5

        try:

            tolerancia = float(
                self.ed_tol.text()
            )

        except:

            tolerancia = 1.0

        n_frames = self.data.n_frames

        n_points = self.data.n_points

        self.movimento_cache = np.ones(
            (n_frames, n_points),
            dtype=bool
        )

        pts = self.data.points

        for frame in range(
            janela,
            n_frames
        ):

            inicio = frame - janela

            trecho = pts[
                inicio:frame + 1
            ]

            diff = np.diff(
                trecho,
                axis=0
            )

            movimento = np.sum(
                np.linalg.norm(
                    diff,
                    axis=2
                ),
                axis=0
            )

            self.movimento_cache[
                frame
            ] = (
                movimento >= tolerancia
            )

    # ==================================================
    # FILTRO PONTOS
    # ==================================================

    def pontos_filtrados(self):

        xyz = self.data.get_frame(
            self.frame_atual
        )

        if not self.chk_estaticos.isChecked():
            return xyz

        if self.movimento_cache is None:
            return xyz

        mask = self.movimento_cache[
            self.frame_atual
        ]

        return xyz[
            mask
        ]

    # ==================================================
    # OVERRIDE DO DESENHO
    # ==================================================

    def obter_pontos_frame(self):

        if not self.data.is_loaded():
            return None

        return self.pontos_filtrados()

    # ==================================================
    # VISTAS
    # ==================================================

    def salvar_vista(self, slot):

        self.views.save_view(
            slot,
            self.camera
        )

        self.statusBar().showMessage(
            f"Vista {slot} salva",
            2000
        )

    def restaurar_vista(self, slot):

        if not self.views.has_view(
            slot
        ):

            QMessageBox.information(
                self,
                "Vista inexistente",
                f"A vista {slot} "
                f"ainda não foi salva."
            )

            return

        estado = (
            self.views.restore_view(
                slot
            )
        )

        self.camera.restore_state(
            estado
        )

        self.atualizar_camera()

        QMessageBox.information(
            self,
            "Vista restaurada",
            f"Vista {slot} restaurada."
        )

    # ==================================================
    # ATALHOS 1..5
    # ==================================================

    def processar_vistas_teclado(
        self,
        tecla,
        mods
    ):

        slots = {
            Qt.Key_1: 1,
            Qt.Key_2: 2,
            Qt.Key_3: 3,
            Qt.Key_4: 4,
            Qt.Key_5: 5
        }

        if tecla not in slots:
            return False

        slot = slots[tecla]

        if mods & Qt.ControlModifier:

            self.salvar_vista(
                slot
            )

        else:

            self.restaurar_vista(
                slot
            )

        return True
        
            
