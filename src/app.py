import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QGroupBox, QComboBox, QLabel, \
    QFileDialog, QLineEdit, QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView

import plotly.graph_objects as go

from src import constants, models, interfaces, utils


class URLButton(QPushButton):

    def __init__(self, *args):
        super().__init__(*args)

        self._url = None

    def get_url(self) -> str:
        print(self._url)

        return self._url

    def set_url(self, url: str):
        self._url = url


class DatasetMenu(interfaces.Window, QWidget):

    def __init__(self, localization: models.Localization = constants.LOCALIZATION.get('EN')):
        super().__init__()

        self._dlg_layout = QGridLayout()
        self._localization = localization
        self._dataset_buttons = {}

        self._is_configured = False
        self.configure()

    def configure(self):
        if not self._is_configured:
            self.setFixedSize(*constants.DATASET_RESOLUTION)

            pos = 0
            for key, value in constants.DATASET_INFO.items():
                button = URLButton(f'{value.name} - {value.size} GB')
                button.set_url(url=value.url)
                button.clicked.connect(button.get_url)

                self._dataset_buttons[key] = button
                self._dlg_layout.addWidget(button, pos, 0)

                pos += 1

            self._set_position()
            self._set_naming()

            self._is_configured = True

    def change_localization(self, language: str):
        if self._localization.language != language:
            self._localization = constants.LOCALIZATION.get(language)
            self._set_naming()

    def _set_position(self):
        self.setLayout(self._dlg_layout)

    def _set_naming(self):
        self.setWindowTitle(self._localization.dataset_menu.window_name)


class MainWindow(interfaces.Window, QMainWindow):

    def __init__(self, localization: models.Localization = constants.LOCALIZATION.get('EN')):
        super().__init__()

        self._localization = localization
        self._path = None
        self._model = None

        self._reader = utils.ImageReader('../dataset', img_size=128, normalize=True, single_class=False)
        self._viewer = utils.ImageViewer(self._reader, mri_downsample=20)

        self._menu_group = QGroupBox()
        self._dataset_group = QGroupBox()
        self._config_group = QGroupBox()
        self._manipulate_group = QGroupBox()
        self._graph_group = QGroupBox()

        self._main_layout = QGridLayout()
        self._menu_layout = QGridLayout()
        self._dataset_layout = QGridLayout()
        self._config_layout = QGridLayout()
        self._manipulate_layout = QGridLayout()
        self._graph_layout = QGridLayout()

        self._open_dataset_button = QPushButton()
        self._download_dataset_button = QPushButton()
        self._open_config_button = QPushButton()
        self._save_config_button = QPushButton()
        self._run_button = QPushButton()

        self._size_policy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)

        self._patient_id = QLineEdit()

        self._mode = QLabel()
        self._segmentator = QLabel()

        self._mode_picker = QComboBox()
        self._neuro_picker = QComboBox()

        self._browser = QWebEngineView(self)

        self._dataset_picker = None

        self._is_configured = False
        self.configure()

    def configure(self):
        if not self._is_configured:
            self.setFixedSize(*constants.MAIN_RESOLUTION)

            self._menu_group.setLayout(self._menu_layout)
            self._dataset_group.setLayout(self._dataset_layout)
            self._config_group.setLayout(self._config_layout)
            self._manipulate_group.setLayout(self._manipulate_layout)
            self._graph_group.setLayout(self._graph_layout)

            self._patient_id.setSizePolicy(self._size_policy)
            self._patient_id.setMaximumWidth(40)
            self._patient_id.setMaxLength(4)

            layout = QWidget()
            layout.setLayout(self._main_layout)
            self.setCentralWidget(layout)

            self._set_position()
            self._set_events()
            self._set_naming()

            self._is_configured = True

    def change_localization(self, language: str):
        if self._localization.language != language:
            self._localization = constants.LOCALIZATION.get(language)
            self._set_naming()

            self._dataset_picker.change_localization(self._localization)

    def download_list(self):
        if self._dataset_picker is None:
            self._dataset_picker = DatasetMenu(self._localization)
        self._dataset_picker.show()

    def show_graph(self):
        fig = self._viewer.get_3d_scan(0, 't1')
        fig = go.Figure(fig)

        self._browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def open_configuration(self):
        configuration_dir = QFileDialog.getOpenFileName(
            parent=self,
            caption=self._localization.main_window.open_config_button,
            directory=os.getenv('HOME'),
            filter='All Files(*);;Text Files(*.txt)',
        )

        if configuration_dir:
            self._model = configuration_dir
            # TODO: create validate model service

    def save_configuration(self):
        if self._model is not None:
            filename, _ = QFileDialog.getSaveFileName(
                parent=self,
                caption=self._localization.main_window.save_config_button,
                directory=os.getenv('HOME'),
                filter='All Files(*);;Text Files(*.txt)',
            )

            if filename:
                with open(filename, 'w') as f:
                    f.write(self._model)

                self.setWindowTitle(f'{self._localization.main_window.app_name} - {filename}')

    def run_button(self):
        if self._path is None:
            raise FileNotFoundError

        if self._model is None:
            self._model = self._neuro_picker.currentText()

        if self._mode_picker.currentText() == self._localization.main_window.single_mode:
            patient_id = self._patient_id.text()
            if patient_id is None:
                raise AttributeError
            self.show_graph()
        elif self._mode_picker.currentText() == self._localization.main_window.train_validate_mode:
            pass
        else:
            pass

    def select_path(self):
        dataset_dir = QFileDialog.getExistingDirectory(
            parent=self,
            caption=self._localization.main_window.open_dataset_button,
            directory=os.getenv('HOME'),
            options=QFileDialog.Option.ShowDirsOnly,
        )

        if dataset_dir:
            self._path = dataset_dir
            # TODO: create validate dir service

    def mode_changer(self):
        if self._mode_picker.currentText() != self._localization.main_window.single_mode:
            self._patient_id.setEnabled(False)
        else:
            self._patient_id.setEnabled(True)

    def _set_position(self):
        self._dataset_layout.addWidget(self._open_dataset_button, 0, 0)
        self._dataset_layout.addWidget(self._download_dataset_button, 1, 0)

        self._config_layout.addWidget(self._open_config_button, 0, 0, 1, 0)
        self._config_layout.addWidget(self._save_config_button, 1, 0, 2, 0)
        self._config_layout.addWidget(self._mode, 3, 0)
        self._config_layout.addWidget(self._mode_picker, 4, 0)
        self._config_layout.addWidget(self._patient_id, 4, 1)
        self._config_layout.addWidget(self._segmentator, 6, 0)
        self._config_layout.addWidget(self._neuro_picker, 7, 0)

        self._manipulate_layout.addWidget(self._run_button, 0, 0)

        self._graph_layout.addWidget(self._browser, 0, 0)

        self._menu_layout.addWidget(self._dataset_group, 0, 0)
        self._menu_layout.addWidget(self._config_group, 1, 0, 2, 0)
        self._menu_layout.addWidget(self._manipulate_group, 3, 0)

        self._main_layout.addWidget(self._menu_group, 0, 0)
        self._main_layout.addWidget(self._graph_group, 0, 1, 0, 5)

    def _set_events(self):
        self._open_dataset_button.clicked.connect(self.select_path)
        self._download_dataset_button.clicked.connect(self.download_list)
        self._open_config_button.clicked.connect(self.open_configuration)
        self._save_config_button.clicked.connect(self.save_configuration)
        self._mode_picker.currentTextChanged.connect(self.mode_changer)
        self._run_button.clicked.connect(self.run_button)

    def _set_naming(self):
        self.setWindowTitle(self._localization.main_window.app_name)

        self._menu_group.setTitle(self._localization.main_window.menu_group)
        self._dataset_group.setTitle(self._localization.main_window.dataset_group)
        self._config_group.setTitle(self._localization.main_window.config_group)
        self._manipulate_group.setTitle(self._localization.main_window.manipulate_group)
        self._graph_group.setTitle(self._localization.main_window.graph_group)

        self._open_dataset_button.setText(self._localization.main_window.open_dataset_button)
        self._download_dataset_button.setText(self._localization.main_window.download_dataset_button)

        self._open_config_button.setText(self._localization.main_window.open_config_button)
        self._save_config_button.setText(self._localization.main_window.save_config_button)
        self._mode.setText(self._localization.main_window.mode)

        self._mode_picker.clear()
        self._mode_picker.addItems(
            [
                self._localization.main_window.single_mode,
                self._localization.main_window.train_validate_mode,
                self._localization.main_window.test_mode
            ]
        )

        self._neuro_picker.clear()
        self._neuro_picker.addItems(constants.segmentators)

        self._segmentator.setText(self._localization.main_window.segmentator)

        self._run_button.setText(self._localization.main_window.run_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
