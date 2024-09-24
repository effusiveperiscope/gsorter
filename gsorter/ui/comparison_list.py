from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
import gsorter as gs
class ComparisonList(QListWidget):
    ComparisonRole = Qt.UserRole + 2
    def __init__(self, set_comparison_cb):
        super().__init__()
        self._group = None
        self.set_comparison_cb = set_comparison_cb

        #self.currentItemChanged.connect(lambda item: print(item))
        self.currentItemChanged.connect(lambda item:
            self.set_comparison_cb(
                item.data(ComparisonList.ComparisonRole)))
        
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