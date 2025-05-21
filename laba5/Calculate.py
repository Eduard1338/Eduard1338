from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QGridLayout




class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        grid = QGridLayout()

        # Создаем виджеты
        self.input_field = QLineEdit()
        self.result_field = QLineEdit()
        self.result_field.setReadOnly(True)
        self.calculate_btn = QPushButton("Вычислить")
        self.calculate_btn.clicked.connect(self.calculate)

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.input_field)
        layout.addWidget(self.calculate_btn)
        layout.addWidget(self.result_field)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def calculate(self):
        try:
            expression = self.input_field.text()
            result = eval(expression)
            self.result_field.setText(str(result))
        except:
            self.result_field.setText("Ошибка вычисления")


app = QApplication([])
window = Calculator()
window.show()
app.exec_()