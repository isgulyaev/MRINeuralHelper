from dataclasses import dataclass
from typing import List


@dataclass
class MainWindowNaming:
    app_name: str
    menu_group: str
    dataset_group: str
    config_group: str
    manipulate_group: str
    graph_group: str
    open_dataset_button: str
    download_dataset_button: str
    open_config_button: str
    save_config_button: str
    mode: str
    single_mode: str
    train_validate_mode: str
    test_mode: str
    segmentator: str
    run_button: str


@dataclass
class DatasetMenuNaming:
    window_name: str


@dataclass
class Localization:
    language: str
    main_window: MainWindowNaming
    dataset_menu: DatasetMenuNaming


@dataclass
class Dataset:
    name: str
    url: str
    size: float
