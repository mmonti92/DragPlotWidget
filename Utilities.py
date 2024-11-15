import numpy as np
import typing as tp


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

    data = 0

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

    return data
