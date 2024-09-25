from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox,
    QStatusBar)
from gsorter.ui.group_tree import GroupTree
from gsorter.ui.comparison_list import ComparisonList
from gsorter.ui.item_grid import ItemGrid
import gsorter as gs
from datetime import datetime

class CentralWidget(QFrame):
    def __init__(self, sorter):
        super().__init__()

        project = sorter.project
        fields = sorter.fields
        self.actions_count = 0

        ext_layout = QVBoxLayout(self)

        internal_frame = QFrame()
        ext_layout.addWidget(internal_frame)
        layout = QHBoxLayout(internal_frame)
        item_grid = ItemGrid(sorter, fields)
        layout.addWidget(item_grid)
        
        item_grid.change_made.connect(self.countAction)

        rl_box = QGroupBox("Comparisons")
        rl_layout = QHBoxLayout(rl_box)
        self.rl = ComparisonList(self, item_grid.setComparison)
        rl_layout.addWidget(self.rl)
        layout.addWidget(rl_box)

        gt_box = QGroupBox("Editing groups")
        gt_layout = QHBoxLayout(gt_box)
        gt = GroupTree(sorter, self.rl.setGroup)
        gt_layout.addWidget(gt)
        sorter.loaded_project.connect(gt.loadProject)
        layout.addWidget(gt_box)

        self.status_bar = QStatusBar()
        ext_layout.addWidget(self.status_bar)
        self.status_bar.showMessage("Status")
        sorter.status.connect(self.statusCb)

        self._sorter = sorter

    def countAction(self, score : int):
        self.actions_count += score
        cfg = self._sorter.config
        if cfg['make_backups'] and (self.actions_count > cfg['backup_threshold']):
            self._sorter.make_backup()
            self.actions_count = 0

    def statusCb(self, msg : str):
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.status_bar.showMessage(current_time + ' $ '+msg)