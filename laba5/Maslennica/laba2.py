import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QCheckBox, QLabel, QHBoxLayout, QFrame)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class PancakeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Масленица")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.left_panel = QVBoxLayout()
        self.right_panel = QVBoxLayout()

        # Путь к папке с изображениями
        self.image_dir = os.path.join(os.path.dirname(__file__), "images")

        # Основное изображение блина
        self.base_pancake = QLabel()
        base_image_path = os.path.join(self.image_dir, "blin.jpg")
        if os.path.exists(base_image_path):
            pixmap = QPixmap(base_image_path)
            pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.base_pancake.setPixmap(pixmap)
        else:
            self.base_pancake.setText("Основное изображение блина не найдено!")

        # Контейнер для добавок
        self.toppings_container = QWidget()
        self.toppings_layout = QVBoxLayout()
        self.toppings_container.setLayout(self.toppings_layout)

        # Слой для композиции изображений
        self.composite_frame = QFrame()
        self.composite_layout = QVBoxLayout()
        self.composite_layout.addWidget(self.base_pancake)
        self.composite_layout.addWidget(self.toppings_container)
        self.composite_frame.setLayout(self.composite_layout)

        self.right_panel.addWidget(self.composite_frame)

        # Создаем чекбоксы с добавками
        self.toppings = {
            "Сметана": "smetana.jpeg",
            "Мёд": "med.jpg",
            "Варенье": "varenie.jpg",
            "Икра": "red-caviar.jpg",
            "Сгущенка": "sg.jpeg"
        }

        self.checkbox_map = {}  # Для связи чекбоксов с их добавками
        self.topping_labels = {}  # Для хранения меток с добавками

        for topping, image_file in self.toppings.items():
            cb = QCheckBox(topping)
            self.left_panel.addWidget(cb)
            self.checkbox_map[cb] = (topping, image_file)
            cb.stateChanged.connect(self.toggle_topping)

            # Создаем метку для добавки (изначально скрыта)
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.hide()
            self.topping_labels[topping] = label
            self.toppings_layout.addWidget(label)

        self.main_layout.addLayout(self.left_panel, 1)
        self.main_layout.addLayout(self.right_panel, 3)
        self.central_widget.setLayout(self.main_layout)

    def toggle_topping(self, state):
        checkbox = self.sender()
        topping, image_file = self.checkbox_map[checkbox]
        label = self.topping_labels[topping]

        if state == Qt.Checked:
            # Показываем добавку
            image_path = os.path.join(self.image_dir, image_file)
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label.setPixmap(pixmap)
                label.show()
            else:
                label.setText(f"Изображение не найдено: {image_file}")
                label.show()
        else:
            # Скрываем добавку
            label.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PancakeApp()
    window.show()
    sys.exit(app.exec_())