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

        ext_layout = QVBoxLayout(self)

        internal_frame = QFrame()
        ext_layout.addWidget(internal_frame)
        layout = QHBoxLayout(internal_frame)
        item_grid = ItemGrid(sorter, fields)
        layout.addWidget(item_grid)

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

    def statusCb(self, msg : str):
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.status_bar.showMessage(current_time + ' $ '+msg)