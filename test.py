from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: black")
        self.setWindowOpacity(0.5)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.showFullScreen()

    ok = QMessageBox.question(None, 'Question', 'Question?')
    if ok == QMessageBox.Yes:
        print('User select Ok')
    else:
        print('User select No')

    # Убираем затемнение
    mw.close()

    app.exec()