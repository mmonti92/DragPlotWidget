import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT,
)


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super().__init__(fig)


class PlotWidget(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.canvas = MplCanvas(self)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.canvas.ax.set_title(title)

    def clear_plot(self):
        self.canvas.ax.clear()
        self.canvas.draw()

    def plot_data(self, x, y, label, color=None):
        self.canvas.ax.plot(x, y, label=label, color=color)
        self.canvas.ax.legend(loc="upper center")
        self.canvas.draw()


if __name__ == "__main__":
    ...
