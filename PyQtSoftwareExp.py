# Maurizio Monti 2024
import sys
import numpy as np

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QCheckBox,
)
from PyQt6.QtCore import Qt

import Utilities as ut
import PlotWidgets as pw


class DragAndDropPlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        # ## Defintitions
        self.setWindowTitle("Drag and Drop Plotter")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel("Drag and drop a file here to plot", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Checkbox for persistence
        self.clear_plot = True  # Initial mode: clear plot
        self.check = QCheckBox("Persistent plot", self)
        self.check.setChecked(False)
        self.check.stateChanged.connect(self.toggle_clear_persist)

        # Set up plot widgets
        self.plot_1 = pw.PlotWidget("Time data", self)
        self.plot_fft = pw.PlotWidget("FFT", self)

        plot_layout = QHBoxLayout()
        plot_layout.addWidget(self.plot_1)
        plot_layout.addWidget(self.plot_fft)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.check)
        main_layout.addLayout(plot_layout)

        # Putting all together
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Enable drag-and-drop
        self.setAcceptDrops(True)

    def toggle_clear_persist(self):
        self.clear_plot = not self.clear_plot

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
            valid_files = []
            for url in urls:
                file_path = url.toLocalFile()
                if file_path.endswith(".txt"):
                    valid_files.append(file_path)
                else:
                    self.label.setText(f"Invalid file skipped: {file_path}")
            if valid_files:
                self.plot_files(valid_files)
            else:
                self.label.setText("No valid files were dropped.")

    def plot_files(self, file_paths):
        try:
            for file_path in file_paths:
                data = ut.Reader(file_path)

                # Check if data has at least two columns for x and y
                if data.shape[1] < 2:
                    self.label.setText(
                        "File must have at least two columns for x and y data."
                    )
                    return

                x = data[0]  # Assume first column as x-axis
                y = data[1]  # Assume second column as y-axis

                # Clear the canvas depending on persistence and plot new data
                if self.clear_plot:
                    self.plot_1.clear_plot()
                    self.plot_fft.clear_plot()
                    self.clear_plot = False

                self.plot_1.plot_data(
                    x,
                    y,
                    label=f"{file_path.split('/')[-1]}",
                )
                self.plot_1.canvas.ax.set_title("Plot from data")
                self.plot_1.canvas.ax.set_xlabel("t[fs]")
                self.plot_1.canvas.ax.set_ylabel("V[$\\mu$V]")

                # FFT & plotting
                fft = np.fft.fft(y)[: len(y) // 2]
                f = np.fft.fftfreq(x.size, np.abs(x[1] - x[0]))[: len(y) // 2]
                self.plot_fft.plot_data(f, np.abs(fft), label=None)

                self.plot_fft.canvas.ax.set_title("FFT")
                self.plot_fft.canvas.ax.set_xlabel("$\\nu$[THz]")
                self.plot_fft.canvas.ax.set_ylabel(
                    "FFT amplitude[Arb. Units]"
                )
                self.plot_fft.canvas.ax.set_xlim(0, 5)
                self.plot_fft.canvas.ax.get_legend().remove()

                self.label.setText(f"Plotting data from: {file_path}")
            self.clear_plot = True
        except Exception as e:
            self.label.setText(f"Failed to plot data: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragAndDropPlotter()
    window.show()
    sys.exit(app.exec())
