from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
import gsorter as gs

# Tree view of project groups
class GroupTree(QTreeWidget):
    GroupRole = Qt.UserRole + 1
    def __init__(self, sorter, group_changed_cb):
        super().__init__()
        self._sorter = sorter
        self.setHeaderHidden(True)
        self.currentItemChanged.connect(self.sCurrentItemChanged)
        self.group_changed_cb = group_changed_cb

    def loadProject(self):
        project = self._sorter.project
        self.clear()
        root = self.invisibleRootItem()
        for group in project.groups:
            item = self.addGroup(root, group)

    def addGroup(self, base_item : QTreeWidgetItem, group : gs.Group):
        group_item = QTreeWidgetItem(self)
        group_item.setData(0, GroupTree.GroupRole, group)
        group_item.setText(0, group.name)
        base_item.addChild(group_item)
        for g in group.groups:
            self.addGroup(group_item, g)
        if group.is_current_group:
            self.setCurrentItem(group_item)
        return group_item

    def sCurrentItemChanged(self,
        current : QTreeWidgetItem,
        previous : QTreeWidgetItem):
        if current is not None:
            group : gs.Group = current.data(0, GroupTree.GroupRole)
            group.is_current_group = True
            self.group_changed_cb(group)
        if previous is not None:
            prev_group : gs.Group = previous.data(0,GroupTree.GroupRole)
            prev_group.is_current_group = False