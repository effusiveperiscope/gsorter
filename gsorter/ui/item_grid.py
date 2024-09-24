from PyQt5.QtWidgets import (QGroupBox, QGridLayout, QLineEdit, QVBoxLayout,
    QFrame, QLabel, QTextEdit, QWidget, QRadioButton)
from PyQt5.QtCore import Qt, QSize
import gsorter as gs
class ItemGridField(QWidget):
    def __init__(self, item, field_id, field_spec):
        super().__init__()
        layout = QVBoxLayout(self)
        self.item = item
        self.field_id = field_id
        self.field_spec = field_spec

        value = item.data[field_id]
        if self.field_spec.field_type == 'multiline':
            widget = QTextEdit(str(value))
            self.gettext = widget.toPlainText
        else:
            widget = QLineEdit(str(value))
            self.gettext = widget.text
        widget.setEnabled(self.field_spec.editable)
        layout.addWidget(widget)

        widget.textChanged.connect(self.textChangedCallback)
    
    def textChangedCallback(self):
        self.item.data[self.field_id] = self.gettext()

class ItemGrid(QGroupBox):
    def __init__(self, 
        sorter,
        fields : list[gs.FieldSpec]):
        super().__init__("Items")
        self.layout = QGridLayout(self)
        self.sorter = sorter
        self._fields = fields
        self.radio_buttons = []
        self.comparison = None

        # Assign consistent columns to each field
        self.column_mapping = {field_id : i for i, field_id in 
            enumerate(self._fields.keys())}
        self.refreshHeaders()
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

    def refreshHeaders(self):
        for field_id, col in self.column_mapping.items():
            self.layout.addWidget(QLabel(field_id),
                0, col+1, Qt.AlignmentFlag.AlignTop)

    def updateSelectedIndex(self, checked):
        for i, button in enumerate(self.radio_buttons):
            if button.isChecked():
                self.comparison.selected_item = i

    def setComparison(self, comparison : gs.Comparison):
        self.clearLayout()
        self.refreshHeaders()
        self.comparison = comparison
        self.radio_buttons = []
        for row, item in enumerate(comparison.data):
            button = QRadioButton(str(row))
            button.clicked.connect(self.updateSelectedIndex)
            self.radio_buttons.append(button)
            self.layout.addWidget(button, row+1, 0,
                Qt.AlignmentFlag.AlignTop)
            for t in item.data.items():
                field_id, value = t
                if not field_id in self._fields:
                    continue
                col = self.column_mapping[field_id]
                self.addField(row+1, col+1, field_id, item)

        if len(self.radio_buttons):
            self.radio_buttons[comparison.selected_item].setChecked(True)
    
    def addField(self, row, col, field_id, item):
        field_spec : gs.FieldSpec = self._fields[field_id]
        self.layout.addWidget(
            ItemGridField(item, field_id, field_spec), row, col,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def clearLayout(self):
        layout = self.layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()