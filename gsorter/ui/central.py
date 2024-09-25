from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox
from gsorter.ui.group_tree import GroupTree
from gsorter.ui.comparison_list import ComparisonList
from gsorter.ui.item_grid import ItemGrid
import gsorter as gs
class CentralWidget(QFrame):
    def __init__(self, sorter):
        super().__init__()

        project = sorter.project
        fields = sorter.fields

        layout = QHBoxLayout(self)
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