from src import models


DATASET_FOLDER = './dataset'
DATASET_INFO = {
    1: models.Dataset(name='BraTS 2020', url='BraTS 2020', size=8),
    2: models.Dataset(name='BraTS 2021', url='BraTS 2021', size=13.7)
}

MAIN_RESOLUTION = (1280, 720)
DATASET_RESOLUTION = (400, 300)

segmentators = ['U-Net', 'BiTr-Unet', 'Custom U-Net']

LOCALIZATION = {
    'EN': models.Localization(
        language='en',
        main_window=models.MainWindowNaming(
            app_name='MRI Neural Helper',
            menu_group='Menu',
            dataset_group='Dataset',
            config_group='Configuration',
            manipulate_group='Manipulators',
            graph_group='Graph',
            open_dataset_button='Open Dataset',
            download_dataset_button='Download Dataset',
            open_config_button='Open Configuration',
            save_config_button='Save Configuration',
            mode='Mode',
            single_mode='Single',
            train_validate_mode='Train/Validate',
            test_mode='Testing',
            segmentator='Segmentator',
            run_button='Run',
        ),
        dataset_menu=models.DatasetMenuNaming(
            window_name='Dataset Menu'
        )
    ),
    'RU': models.Localization(
        language='ru',
        main_window=models.MainWindowNaming(
            app_name='MRI Neural Helper',
            menu_group='Меню управления',
            dataset_group='Параметры датасета',
            config_group='Конфигуратор',
            manipulate_group='Стартовые операции',
            graph_group='Результат',
            open_dataset_button='Открыть датасет',
            download_dataset_button='Загрузить датасет',
            open_config_button='Открыть конфигурацию',
            save_config_button='Сохранить конфигурацию',
            mode='Выбор режима работы',
            single_mode='Одиночный',
            train_validate_mode='Обучение/Тестирование',
            test_mode='Тестирование',
            segmentator='Выбор сегментатора',
            run_button='Запуск',
        ),
        dataset_menu=models.DatasetMenuNaming(
            window_name='Список датасетов'
        )
    )
}
