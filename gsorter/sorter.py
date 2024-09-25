from gsorter.project import Project
from gsorter.field import FieldSpec
from gsorter.ui.window import MainWindow
from gsorter.item import Item
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
from omegaconf import OmegaConf
import sys
import time
import os

CONFIG_PATH = 'conf.yaml'
class GSorter(QObject):
    loaded_project = pyqtSignal()
    status = pyqtSignal(str)

    def __init__(self,
    project : Project,
    fields : dict[str, FieldSpec]):
        super().__init__()
        self.fields = fields
        self.project : Project = project
        self.config = OmegaConf.load(CONFIG_PATH)
        self.init_item_timestamps()

    def init_item_timestamps(self):
        current_timestamp = time.time()
        def init_item_timestamp(item: Item):
            for field_id in self.fields.keys():
                if field_id in item.modification_timestamps:
                    continue
                # Change empty to current timestamp
                item.modification_timestamps[field_id] = current_timestamp
        
        def init_comparison_timestamp(comparison):
            comparison.modification_timestamp = current_timestamp

        for g in self.project.groups:
            g.on_leaf_items(init_item_timestamp)
            g.on_leaf_comparisons(init_comparison_timestamp)

    def save(self, file_path, set_last_file=False):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.project.model_dump_json())
            self.status.emit(f"Saved to {file_path}")
        if set_last_file:
            self.config['last_file'] = file_path

    def make_backup(self):
        if not os.path.exists(self.config['backup_dir']):
            os.makedirs(self.config['backup_dir'])
        file_path = os.path.join(self.config['backup_dir'],
            self.project.name + str(int(time.time())) + '.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.project.model_dump_json())
            self.status.emit(f"Saved backup to {file_path}")

    def load(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = f.read()
            self.status.emit(f"Loaded from {file_path}")
        self.config['last_file'] = file_path
        self.project = Project.model_validate_json(json_data)
        self.loaded_project.emit()

    def cleanup(self):
        OmegaConf.save(self.config, f=CONFIG_PATH)

    def ui_run(self):
        app = QApplication(sys.argv)
        window = MainWindow(self)
        window.show()
        if self.config.get('last_file') and os.path.exists(
            self.config['last_file']):
            self.load(self.config['last_file'])
        else:
            self.loaded_project.emit()
        ret = app.exec_()
        self.cleanup()
        return ret