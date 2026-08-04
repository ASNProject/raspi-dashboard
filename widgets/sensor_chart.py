from collections import deque

from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QBrush,
    QPen,
)

from PySide6.QtCore import Qt, QMargins
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QLabel

from core.config_manager import Config
from widgets.card import Card


class SensorChart(Card):

    MAX_POINTS = 50

    def __init__(self):
        super().__init__()

        self.series = {}
        self.buffers = {}

        self.title = QLabel("Realtime Sensor")
        self.title.setObjectName("CardTitle")

        self.layout.addWidget(self.title)

        # ============================================
        # Chart
        # ============================================

        self.chart = QChart()

        self.chart.legend().setVisible(True)

        self.chart.setMargins(QMargins(10, 10, 10, 10))

        self.chart.setAnimationOptions(QChart.NoAnimation)

        # Background
        self.chart.setBackgroundVisible(True)
        self.chart.setBackgroundBrush(QBrush(QColor("#2D2D30")))

        self.chart.setPlotAreaBackgroundVisible(True)
        self.chart.setPlotAreaBackgroundBrush(
            QBrush(QColor("#2D2D30"))
        )

        self.chart.legend().setBackgroundVisible(False)

        # ============================================
        # Axis X
        # ============================================

        self.axisX = QValueAxis()
        self.axisX.setRange(0, self.MAX_POINTS)
        self.axisX.setLabelFormat("%d")
        self.axisX.setGridLineVisible(False)

        # ============================================
        # Axis Y
        # ============================================

        self.axisY = QValueAxis()
        self.axisY.setRange(0, 100)
        self.axisY.setLabelFormat("%d")

        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

        # ============================================
        # Chart Style
        # ============================================

        self.chart.legend().setLabelBrush(
            QBrush(QColor("#FFFFFF"))
        )

        self.axisX.setLabelsBrush(
            QBrush(QColor("#FFFFFF"))
        )

        self.axisY.setLabelsBrush(
            QBrush(QColor("#FFFFFF"))
        )

        pen = QPen(QColor("#808080"))

        self.axisX.setLinePen(pen)
        self.axisY.setLinePen(pen)

        self.axisX.setGridLinePen(pen)
        self.axisY.setGridLinePen(pen)

        # ============================================
        # Create Series From Config
        # ============================================

        self.create_series()

        # ============================================
        # Chart View
        # ============================================

        self.chartView = QChartView(self.chart)

        self.chartView.setRenderHint(QPainter.Antialiasing)

        self.chartView.setMinimumHeight(320)

        self.chartView.setStyleSheet("""
        QChartView{
            background:#2D2D30;
            border:none;
        }
        """)

        self.layout.addWidget(self.chartView)

    # =====================================================
    # Create Series
    # =====================================================

    def create_series(self):

        sensors = Config.get(
            "sensor",
            "cards",
            default=[],
        )

        default_colors = [
            "#ff6b6b",
            "#4dabf7",
            "#51cf66",
            "#ffd43b",
            "#845ef7",
            "#f06595",
            "#20c997",
            "#fd7e14",
            "#868e96",
        ]

        for index, sensor in enumerate(sensors):

            key = sensor["key"]

            color = sensor.get(
                "color",
                default_colors[index % len(default_colors)],
            )

            series = QLineSeries()
            series.setName(sensor["title"])

            self.chart.addSeries(series)

            series.attachAxis(self.axisX)
            series.attachAxis(self.axisY)

            self.series[key] = series
            self.buffers[key] = deque(maxlen=self.MAX_POINTS)

    # =====================================================
    # Update Data
    # =====================================================

    def update_data(self, values: dict):

        max_value = 0

        # Simpan data
        for key, value in values.items():

            if key not in self.buffers:
                continue

            self.buffers[key].append(float(value))

        # Gambar ulang semua series
        for key, series in self.series.items():

            series.clear()

            for i, value in enumerate(self.buffers[key]):

                series.append(i, value)

                if value > max_value:
                    max_value = value

        self.axisX.setRange(
            0,
            self.MAX_POINTS,
        )

        self.axisY.setRange(
            0,
            max(
                100,
                max_value + 10,
            ),
        )