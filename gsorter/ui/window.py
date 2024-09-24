from PyQt5.QtWidgets import QMainWindow
from gsorter.ui.central import CentralWidget
class MainWindow(QMainWindow):
    def __init__(self, sorter):
        super().__init__()
        project = sorter.project
        if len(project.name):
            title = f'gsorter: {project.name}'
        else:
            title = 'gsorter'
        self.setWindowTitle(title)
        self.setCentralWidget(CentralWidget(sorter))