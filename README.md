1. Описание программного обеспечения.
  MRINeuralHelper - программное обеспечение для агрегирования нейронных сетей при решении задачи конкурса BRaTS. В качестве основы концепции лежит интерфейс, под который подводятся все нейронные сети и загружаются в приложение для работы. ПО должно обеспечивать отрисовку датасета, анализ и сегментацию датасета, а также классификацию опухолей.
2. Декомпозиция функциональности.
   1. Интерфейс для нейронных сетей.
   2. Набор базовых нейросетей.
   3. Графический интерфейс.
   4. Отрисовка датасета.
   5. Сегментация и анализ датасета.
   6. Стэк: Python 3.11 + GUI (tkinter, wxpython, kivy, pysimplegui, compose-multiplatform).
3. Развитие существующего концепта.
   1. Формирование списка метрик для аналитики датасета.
   2. Использование референсов графического отображения из программ-аналогов.
4. Написание прототипа.
  Написание прототипа включает работающую программу, которая может выполнять все базовые операции. При написании первого прототипа будет использоваться Python.
1. Описание планов и задач по развитию разработки.
   1. Модульная система по типу vtk: возможность накладывать фильтры, решения задачи различных нейросетей друг на друга - как развитие идеи, дополнить сегментацию и классификацию в пайплайн.
   2. Трансляция на другой язык программирования (C++).
