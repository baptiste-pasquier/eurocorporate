from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QCalendarWidget


class CalendarWidgetPerso(QCalendarWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.highlight = []
        self.m_outlinePen = QPen()
        self.m_outlinePen.setColor(Qt.red)
        self.m_Brush = QBrush()
        self.m_Brush.setColor(Qt.transparent)

    def paintCell(self, painter, rect, date):
        painter.setRenderHint(QPainter.Antialiasing, True)

        QCalendarWidget.paintCell(self, painter, rect, date)
        if date in self.highlight:
            painter.save()
            painter.setPen(self.m_outlinePen)
            painter.setBrush(self.m_Brush)
            painter.drawRect(rect.adjusted(0, 0, -1, -1))
            painter.restore()
