"""Report and note dialog."""

from functools import partial

from ..core.reports import append_message
from .generated.report_dialog import Ui_ReportDialog
from .qt import QMainWindow, Qt


class ReportDialog(QMainWindow):
    def __init__(self, message_type, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        self.ui = Ui_ReportDialog()
        self.ui.setupUi(self)
        self.message_type = message_type

        self.selected_item = tuple(parent.get_selected_item_data())
        self.ui.lineEdit.setText(parent.get_object_outline_path(self.selected_item))
        if message_type == "note":
            self.setWindowTitle("Create note")
            self.ui.spinBox_hours.setDisabled(True)

        self.ui.pushButton_cancel.pressed.connect(self.close)
        self.ui.pushButton_ok.pressed.connect(partial(self.submit, parent))

    def submit(self, parent):
        if not self.selected_item:
            self.close()
            return

        append_message(
            self.selected_item[1],
            self.selected_item[0],
            self.message_type,
            self.ui.textEdit_maintext.toPlainText(),
            self.ui.spinBox_hours.value(),
        )
        parent.update_report_note()
        self.close()
