import tkinter as tk
from enum import Enum
from tkinter import ttk, DISABLED
from PIL import ImageTk, Image

# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GUISize(int, Enum):
    WIN_W = 1280
    WIN_H = 720
    SIDEBAR_W = 200
    SIDEBAR_H = 720
    GRAPHBAR_W = 400
    GRAPHBAR_H = 360
    STATBAR_W = 400
    STATBAR_H = 360
    CANVAS_W = 680
    CANVAS_H = 720


class MRIHelperGUI:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.sidebar = tk.Frame(
            self.window,
            width=GUISize.SIDEBAR_W.value,
            height=GUISize.SIDEBAR_H.value,
            bd=4,
            relief=tk.GROOVE
        )
        self.graphbar = tk.Frame(
            self.window,
            width=GUISize.GRAPHBAR_W.value,
            height=GUISize.GRAPHBAR_H.value,
            bd=4,
            relief=tk.GROOVE
        )
        self.statbar = tk.Frame(
            self.window,
            width=GUISize.STATBAR_W.value,
            height=GUISize.STATBAR_H.value,
            bd=4,
            relief=tk.GROOVE
        )
        self.canvas = tk.Canvas(
            self.window,
            width=GUISize.CANVAS_W.value,
            height=GUISize.CANVAS_H.value,
            bg="#012",
            relief=tk.GROOVE
        )

        self.open_dataset = tk.Button(self.sidebar, text="Открыть датасет")
        self.download_dataset = tk.Button(self.sidebar, text="Скачать датасет")
        self.select_model = tk.Label(self.sidebar, text="Выбор модели")
        self.combobox_mode = ttk.Combobox(self.sidebar)
        self.combobox_mode.bind("<<ComboboxSelected>>")
        self.train_model = tk.Button(self.sidebar, text="Обучить модель")

        self.btb_run = tk.Button(self.sidebar, text="Запуск")
        self.btn_pause = tk.Button(self.sidebar, text="Пауза")
        self.btn_pause.config(state=DISABLED)
        self.btn_result = tk.Button(self.sidebar, text="Результат")
        self.btn_result.config(state=DISABLED)
        self.btn_openconfig = tk.Button(self.sidebar, text="Открыть конфиг")
        self.btn_saveconfig = tk.Button(self.sidebar, text="Сохранить конфиг")

        _3d_model = Image.open('/home/ivang/Pictures/Снимки экрана/Снимок экрана от 2023-06-07 13-28-46.png')
        _3d_model = _3d_model.resize((GUISize.CANVAS_W.value, GUISize.CANVAS_H.value))
        _3d_image = ImageTk.PhotoImage(_3d_model)

        _classes_definition = Image.open('/home/ivang/Pictures/Снимки экрана/Снимок экрана от 2023-06-07 13-17-29.png')
        _classes_definition = _classes_definition.resize((GUISize.GRAPHBAR_W.value - 10, GUISize.GRAPHBAR_H.value - 10))
        _classes_image = ImageTk.PhotoImage(_classes_definition)

        self.main_visualize = tk.Label(self.canvas, image=_3d_image)
        self.main_visualize.image = _3d_image

        self.classes = tk.Label(self.graphbar, image=_classes_image)
        self.classes.image = _classes_image

        self.stat_name = tk.Label(self.statbar, text='Статистика')
        self.stat_1 = tk.Label(self.statbar, text='scores: 0.511904761904762 ROC AUC')
        self.stat_2 = tk.Label(self.statbar, text='scores: 0.553968253968254 ROC AUC')
        self.stat_3 = tk.Label(self.statbar, text='scores: 0.5746031746031747 ROC AUC')
        self.stat_4 = tk.Label(self.statbar, text='average: 0.5738095238095238 ROC AUC')

    def configurate(self) -> None:
        self.window.config(width=GUISize.WIN_W.value, height=GUISize.WIN_H.value)
        self.window.resizable(False, False)
        self.window.title("MRI DL Helper")
        self.sidebar.place(x=0, y=0)
        self.graphbar.place(x=GUISize.SIDEBAR_W.value, y=0)
        self.statbar.place(x=GUISize.SIDEBAR_W.value, y=GUISize.STATBAR_H.value)
        self.canvas.place(x=GUISize.SIDEBAR_W.value + GUISize.GRAPHBAR_W.value, y=0)

        self.open_dataset.place(x=10, y=25)
        self.download_dataset.place(x=10, y=55)
        self.select_model.place(x=10, y=250)
        self.combobox_mode.place(x=12, y=275)
        self.train_model.place(x=10, y=300)

        self.btb_run.place(x=12, y=455, width=int(GUISize.SIDEBAR_W.value / 3))
        self.btn_pause.place(x=12, y=485, width=int(GUISize.SIDEBAR_W.value / 3))
        self.btn_result.place(x=12, y=515, width=int(GUISize.SIDEBAR_W.value / 2))
        self.btn_openconfig.place(x=12, y=640)
        self.btn_saveconfig.place(x=12, y=665)

        self.main_visualize.place(x=0, y=0)
        self.classes.place(x=0, y=0)

        self.stat_name.place(x=50, y=75)
        self.stat_1.place(x=50, y=100)
        self.stat_2.place(x=50, y=125)
        self.stat_3.place(x=50, y=150)
        self.stat_4.place(x=50, y=175)

    def start(self) -> None:
        self.configurate()
        self.window.mainloop()


if __name__ == '__main__':
    app = MRIHelperGUI()
    app.start()
