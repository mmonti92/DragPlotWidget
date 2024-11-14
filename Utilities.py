import numpy as np
import typing as tp
import inspect
import sys
import warnings as wn


def Reader(
    file: str,
    comments: str = "%",
    delimiter: str = "\t",
    transpose: bool = True,
    *args: tp.Optional,
    **kwargs: tp.Optional,
) -> np.ndarray:
    """
    A wrapper around numpy genfromtxt to read text files

    """

    caller = inspect.getframeinfo(sys._getframe(1)).filename
    data = 0
    try:
        data = np.genfromtxt(
            file,
            unpack=False,
            comments=comments,
            delimiter=delimiter,
            *args,
            **kwargs,
        )
        if "names" not in kwargs:
            # datanew = data[:, ~np.all(np.isnan(data), axis=0)]
            datanew = np.nan_to_num(data)
            data = 0
        else:
            datanew = data
        if transpose:
            data = np.transpose(datanew)
        else:
            data = datanew
    except IOError:
        raise IOError(f"File {file} not found by {caller}")

    return data


def FFT(
    xData: np.ndarray, yData: np.ndarray, xUnit: str = ""
) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the FFT, wrapper around numpy fft

    Parameters
    ----------
    xData: numpy array
        time-axis data (not necessarily in a strictly time unit)
    yData: numpy array
        y data
    xUnit: str
        unit of the x axis,
    """
    # computes the FFT of the data and returns the frequency and the spectrum
    # of the FFT
    # xUnit used to convert the xData in frequency depending on the unit of
    # the x (mm or seconds, not implemented yet)
    yFourier = np.fft.fft(yData)
    fftLen = len(yFourier)
    yFourier = yFourier[0 : int((fftLen / 2 + 1))]
    match xUnit:
        case "OD":
            conv = 0.2998
        case "mm":
            conv = 0.1499
        case "t" | "ps":
            conv = 1.0
        case _:
            wn.warn("Warnings: format not specified, default used")
            conv = 1.0

    timeStep = abs(xData[fftLen - 1] - xData[0]) / (fftLen - 1) / conv
    freq = np.array(list(range(int(fftLen / 2 + 1)))) / timeStep / fftLen

    return freq, yFourier


if __name__ == "__main__":
    ...
