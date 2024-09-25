from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QMessageBox)
from PyQt5.QtGui import QIcon
from gsorter.ui.central import CentralWidget
class MainWindow(QMainWindow):
    def __init__(self, sorter):
        super().__init__()
        self._sorter = sorter
        project = sorter.project
        self.updateTitle()
        central_widget = CentralWidget(sorter)
        central_widget.item_grid.change_made.connect(lambda score:
            self.updateTitle())
        self.setCentralWidget(central_widget)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu(QIcon(), 'File')

        self.save_action = QAction(QIcon(), 'Save')
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.saveFn)
        file_menu.addAction(self.save_action)
        self.save_as_action = QAction(QIcon(), 'Save as')
        self.save_as_action.setShortcut('Ctrl+Shift+S')
        self.save_as_action.triggered.connect(self.saveAsFn)
        file_menu.addAction(self.save_as_action)
        self.set_primary_path = QAction(QIcon(), 'Set primary save')
        self.set_primary_path.setShortcut('Ctrl+Shift+P')
        self.set_primary_path.triggered.connect(self.setPrimarySaveFn)
        self.open_action = QAction(QIcon(), 'Open')
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.triggered.connect(self.openFn)
        file_menu.addAction(self.open_action)

    def updateTitle(self):
        project = self._sorter.project
        if len(project.name):
            title = f'gsorter: {project.name}'
        else:
            title = 'gsorter'
        if 'primary_save_path' in project.userdata:
            title += f' ({project.userdata["primary_save_path"]})'
        if self._sorter.dirty_flag:
            title += '*'
        self.setWindowTitle(title)

    def updateProject(self):
        self.updateTitle()

    def setPrimarySaveFn(self):
        project = self._sorter.project
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save project",
            project.userdata.get('primary_save_path', project.name+'.json'), 
            "JSON Files (*.json);;All Files (*)",
            options=options)
        if len(file_path):
            project.userdata['primary_save_path'] = file_path
        self.updateProject()

    def promptPrimarySave(self, file_path):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Set primary save")
        msg_box.setText(f"Set {file_path} to primary save path?")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        response = msg_box.exec_()
        return (response == QMessageBox.StandardButton.Yes)

    def saveFn(self):
        project = self._sorter.project
        if not 'primary_save_path' in project.userdata:
            file_path = self.saveAsFn(primary_prompt=True)
        else:
            self._sorter.save(
                project.userdata['primary_save_path'], set_last_file=True)
        self._sorter.dirty_flag = False
        self.updateProject()

    # Should return save path
    def saveAsFn(self, primary_prompt=False):
        project = self._sorter.project
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save project",
            project.userdata.get('primary_save_path', project.name+'.json'), 
            "JSON Files (*.json);;All Files (*)",
            options=options)
        if len(file_path):
            if primary_prompt and self.promptPrimarySave(file_path):
                project.userdata['primary_save_path'] = file_path
                self._sorter.save(file_path=file_path, set_last_file=True)
            else:
                self._sorter.save(file_path=file_path)
        return file_path

    def openFn(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open project", "",
            "JSON Files (*.json);;All Files (*)",
            options=options)
        # TODO error handling here.
        if len(file_path):
            self._sorter.load(file_path)
            self.updateProject()
        