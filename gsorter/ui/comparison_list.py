from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
import gsorter as gs
class ComparisonList(QListWidget):
    ComparisonRole = Qt.UserRole + 2
    def __init__(self, sorter, set_comparison_cb):
        super().__init__()
        self._group = None
        self._sorter = sorter
        self.set_comparison_cb = set_comparison_cb

        self.currentItemChanged.connect(self.updateGroupItem)
        self.currentRowChanged.connect(self.updateGroup)

    def updateGroupItem(self, item : gs.Item | None):
        if item is not None:
            self.set_comparison_cb(
                item.data(ComparisonList.ComparisonRole))

    def updateGroup(self, row : int):
        if self._group is not None:
            self._group.current_comparison = row
        
    def setGroup(self, group : gs.Group):
        self.clear()
        self._group = group
        if group is None:
            return
        for comparison_id, comparison in group.comparisons.items():
            item = QListWidgetItem()
            item.setText(comparison_id)
            item.setData(ComparisonList.ComparisonRole, comparison)
            self.addItem(item)

        if self._group.current_comparison is not None:
            self.setCurrentRow(self._group.current_comparison)