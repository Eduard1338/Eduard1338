import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QInputDialog)
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt


class FlagGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор случайного флага")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Кнопка для запроса количества цветов
        self.generate_button = QPushButton("Сгенерировать флаг")
        self.generate_button.clicked.connect(self.generate_flag)
        self.layout.addWidget(self.generate_button)

        # Метка для изображения флага
        self.flag_label = QLabel()
        self.flag_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.flag_label)

        self.central_widget.setLayout(self.layout)

    def generate_flag(self):
        # Запрашиваем у пользователя количество цветов
        num_colors, ok = QInputDialog.getInt(
            self, "Количество цветов", "Введите количество цветов (2-10):",
            3, 2, 10, 1
        )

        if not ok:
            return

        # Создаем изображение флага
        flag_width = 300
        flag_height = 200
        stripe_height = flag_height // num_colors

        # Создаем QPixmap для рисования
        pixmap = QPixmap(flag_width, flag_height)
        painter = QPainter(pixmap)

        # Рисуем полосы
        for i in range(num_colors):
            # Генерируем случайный цвет
            color = QColor(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            painter.setBrush(color)
            painter.setPen(color)

            # Рисуем полосу
            y = i * stripe_height
            painter.drawRect(0, y, flag_width, stripe_height)

        painter.end()

        # Отображаем флаг
        self.flag_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlagGenerator()
    window.show()
    sys.exit(app.exec_())