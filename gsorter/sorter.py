from gsorter.project import Project
from gsorter.field import FieldSpec
from gsorter.ui.window import MainWindow
from gsorter.item import Item
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
import sys
import time

class GSorter(QObject):
    loaded_project = pyqtSignal()

    def __init__(self,
    project : Project,
    fields : dict[str, FieldSpec]):
        super().__init__()
        self.fields = fields
        self.project : Project = project
        self.init_item_timestamps()

    def init_item_timestamps(self):
        current_timestamp = time.time()
        def init_item_timestamp(item: Item):
            for field_id in self.fields.keys():
                if field_id in item.modification_timestamps:
                    continue
                # Change empty to current timestamp
                item.modification_timestamps[field_id] = current_timestamp
        for g in self.project.groups:
            g.on_leaf_items(init_item_timestamp)

    def save(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.project.model_dump_json())

    def load(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = f.read()
        self.project = Project.model_validate_json(json_data)
        self.loaded_project.emit()

    def ui_run(self):
        app = QApplication(sys.argv)
        window = MainWindow(self)
        window.show()
        return app.exec_()