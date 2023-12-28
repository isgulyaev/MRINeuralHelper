import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QGroupBox, QComboBox, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView

import plotly.graph_objects as go

from src.utils import ImageReader, ImageViewer3d
from src import constants, models


class DatasetMenu(QWidget):

    def __init__(self, localization: models.DatasetMenuNaming):
        super().__init__()
        self.dlg_layout = QGridLayout()
        self.setFixedSize(*constants.DATASET_RESOLUTION)

        self.localization = None

        pos = 0
        for key, value in constants.DATASET_INFO.items():
            dataset_button = QPushButton(f'{value.name} - {value.size} GB')
            self.dlg_layout.addWidget(dataset_button, pos, 0)
            pos += 1

        self.setLayout(self.dlg_layout)

        self.set_localization(localization)
        self.set_naming()

    def set_naming(self):
        self.setWindowTitle(self.localization.window_name)

    def set_localization(self, localization: models.DatasetMenuNaming):
        self.localization = localization


class MainWindow(QMainWindow):
    def __init__(self, path: str, localization: models.Localization = constants.LOCALIZATION.get('EN')):
        super().__init__()

        self.localization = localization

        self.path = path

        self.reader = ImageReader(self.path, img_size=128, normalize=True, single_class=False)
        self.viewer = ImageViewer3d(self.reader, mri_downsample=20)

        self.setFixedSize(*constants.MAIN_RESOLUTION)

        self.main_layout = QGridLayout()

        self.menu_group = QGroupBox()
        self.dataset_group = QGroupBox()
        self.config_group = QGroupBox()
        self.manipulate_group = QGroupBox()
        self.graph_group = QGroupBox()

        self.menu_layout = QGridLayout()
        self.dataset_layout = QGridLayout()
        self.config_layout = QGridLayout()
        self.manipulate_layout = QGridLayout()
        self.graph_layout = QGridLayout()

        self.open_dataset_button = QPushButton()
        self.download_dataset_button = QPushButton()
        self.dataset_layout.addWidget(self.open_dataset_button, 0, 0)
        self.dataset_layout.addWidget(self.download_dataset_button, 1, 0)

        self.open_config_button = QPushButton()
        self.save_config_button = QPushButton()
        self.mode = QLabel()
        self.mode_picker = QComboBox()
        self.segmentator = QLabel()
        self.neuro_picker = QComboBox()
        self.neuro_picker.addItems(constants.segmentators)
        self.config_layout.addWidget(self.open_config_button, 0, 0)
        self.config_layout.addWidget(self.save_config_button, 1, 0, 2, 0)
        self.config_layout.addWidget(self.mode, 3, 0)
        self.config_layout.addWidget(self.mode_picker, 4, 0)
        self.config_layout.addWidget(self.segmentator, 5, 0)
        self.config_layout.addWidget(self.neuro_picker, 6, 0)

        self.run_button = QPushButton()
        self.manipulate_layout.addWidget(self.run_button, 0, 0)

        self.browser = QWebEngineView(self)
        self.graph_layout.addWidget(self.browser, 0, 0)

        self.menu_group.setLayout(self.menu_layout)
        self.dataset_group.setLayout(self.dataset_layout)
        self.config_group.setLayout(self.config_layout)
        self.manipulate_group.setLayout(self.manipulate_layout)
        self.graph_group.setLayout(self.graph_layout)

        self.menu_layout.addWidget(self.dataset_group, 0, 0)
        self.menu_layout.addWidget(self.config_group, 1, 0, 2, 0)
        self.menu_layout.addWidget(self.manipulate_group, 3, 0)

        self.main_layout.addWidget(self.menu_group, 0, 0)
        self.main_layout.addWidget(self.graph_group, 0, 1, 0, 5)

        layout = QWidget()
        layout.setLayout(self.main_layout)
        self.setCentralWidget(layout)

        self.download_dataset_button.clicked.connect(self.download_list)
        self.run_button.clicked.connect(self.show_graph)

        self.w = None

        self.set_naming()

    def download_list(self):
        if self.w is None:
            self.w = DatasetMenu(self.localization.dataset_menu)
        self.w.show()

    def show_graph(self):
        fig = self.viewer.get_3d_scan(0, 't1')
        fig = go.Figure(fig)

        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def set_naming(self):
        self.setWindowTitle(self.localization.main_window.app_name)

        self.menu_group.setTitle(self.localization.main_window.menu_group)
        self.dataset_group.setTitle(self.localization.main_window.dataset_group)
        self.config_group.setTitle(self.localization.main_window.config_group)
        self.manipulate_group.setTitle(self.localization.main_window.manipulate_group)
        self.graph_group.setTitle(self.localization.main_window.graph_group)

        self.open_dataset_button.setText(self.localization.main_window.open_dataset_button)
        self.download_dataset_button.setText(self.localization.main_window.download_dataset_button)

        self.open_config_button.setText(self.localization.main_window.open_config_button)
        self.save_config_button.setText(self.localization.main_window.save_config_button)
        self.mode.setText(self.localization.main_window.mode)

        self.mode_picker.clear()
        self.mode_picker.addItems(
            [
                self.localization.main_window.single_mode,
                self.localization.main_window.train_validate_mode,
                self.localization.main_window.test_mode
            ]
        )

        self.segmentator.setText(self.localization.main_window.segmentator)

        self.run_button.setText(self.localization.main_window.run_button)

        if self.w:
            self.w.set_naming()

    def change_localization(self, language: str):
        if self.localization.language != language:
            self.localization = constants.LOCALIZATION.get(language)
            self.set_naming()


app = QApplication(sys.argv)

window = MainWindow(path='../dataset')
window.show()

app.exec()
