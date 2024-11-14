import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QCheckBox,
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT,
)

import Utilities as ut


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super().__init__(fig)


class DragAndDropPlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drag and Drop Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Label to instruct users to drag files here
        self.label = QLabel("Drag and drop a file here to plot", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Button to toggle persistence
        self.clear_plot = True  # Initial mode: clear plot

        self.check = QCheckBox("Persistent plot", self)
        # self.toggle_button = QPushButton("Switch to Persistent Plot", self)
        # self.toggle_button.clicked.connect(self.toggle_clear_persist)
        self.check.setChecked(False)
        self.check.stateChanged.connect(self.toggle_clear_persist)

        # Set up matplotlib canvas for plotting
        self.canvas = MplCanvas(self)
        self.canvas_fft = MplCanvas(self)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar_fft = NavigationToolbar2QT(self.canvas_fft, self)

        plot_layout_1 = QVBoxLayout()
        plot_layout_1.addWidget(self.toolbar)
        plot_layout_1.addWidget(self.canvas)

        plot_layout_fft = QVBoxLayout()
        plot_layout_fft.addWidget(self.toolbar_fft)
        plot_layout_fft.addWidget(self.canvas_fft)

        plot_layout = QHBoxLayout()
        plot_layout.addLayout(plot_layout_1)
        plot_layout.addLayout(plot_layout_fft)

        # Set up layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.check)
        main_layout.addLayout(plot_layout)

        # Set up central widget
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Enable drag-and-drop
        self.setAcceptDrops(True)

    def toggle_clear_persist(self):
        self.clear_plot = not self.clear_plot
        # if self.clear_plot:
        #     self.toggle_button.setText("Switch to Persistent Plot")
        # else:
        #     self.toggle_button.setText("Switch to Clear Plot")

    # Override dragEnterEvent to accept files
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    # Override dropEvent to handle dropped files
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[
                0
            ].toLocalFile()  # Get the file path of the dropped file
            # if file_path.endswith(".csv"):
            self.plot_file(file_path)
            # else:
            #     self.label.setText("Please drop a CSV file.")

    # Function to read and plot  file
    def plot_file(self, file_path):
        try:
            data = ut.Reader(file_path)

            # Check if data has at least two columns for x and y
            if data.shape[1] < 2:
                self.label.setText(
                    "File must have at least two columns for x and y data."
                )
                return

            x = data[0]  # Assume first column as x-axis
            y = data[1]  # Assume second column as y-axis

            # Clear the canvas and plot new data
            if self.clear_plot:
                self.canvas.ax.clear()
                self.canvas_fft.ax.clear()
            self.canvas.ax.plot(
                x,
                y,
                # marker="o",
                label=f"{file_path.split('/')[-1]}",
            )
            self.canvas.ax.set_title("Plot from data")
            self.canvas.ax.set_xlabel("t[fs]")
            self.canvas.ax.set_ylabel("V[$\\mu V$]")

            f, fft = ut.FFT(x, y, "t")
            self.canvas_fft.ax.plot(
                f,
                np.abs(fft),
                # marker="o",
                # label=f"Processed ({file_path.split('/')[-1]})",
            )
            self.canvas_fft.ax.set_title("FFT")
            self.canvas_fft.ax.set_xlabel("\\nu[THz]")
            self.canvas_fft.ax.set_ylabel("FFT amplitude[Arb. Units]")
            self.canvas_fft.ax.set_xlim(0, 5)

            if not self.clear_plot:
                self.canvas.ax.legend()
            self.canvas.draw()
            self.canvas_fft.draw()

            self.label.setText(f"Plotting data from: {file_path}")
        except Exception as e:
            self.label.setText(f"Failed to plot data: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragAndDropPlotter()
    window.show()
    sys.exit(app.exec())
