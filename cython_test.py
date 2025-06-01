from PySide6 import QtCore, QtWidgets


def test_slot(arg: int):
    print(f"Slot 1 called with {type(arg)} = {arg}")


def test_slot_untyped(arg):
    print(f"Slot 2 called with {type(arg)} = {arg}")
    return arg


def main():
    print("Starting the application...")
    app = QtWidgets.QApplication([])

    # Create a simple widget to test the slot
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)

    button = QtWidgets.QPushButton("Click Me")

    button.clicked.connect(lambda: test_slot(0.5))  # Connect the button click to the slot
    button.clicked.connect(lambda: test_slot_untyped(0.5))

    layout.addWidget(button)
    widget.setLayout(layout)
    widget.show()

    app.exec()