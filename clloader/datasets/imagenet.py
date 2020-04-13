import abc
import os
from typing import List, Tuple, Union

import numpy as np

from clloader.datasets import ImageFolderDataset
from torchvision import datasets as torchdata


class ImageNet1000(ImageFolderDataset):

    def _download(self):
        if not os.path.exists(self.train_folder) or not os.path.exists(self.test_folder):
            raise IOError(
                "You must download yourself the ImageNet dataset."
                " Please go to http://www.image-net.org/challenges/LSVRC/2012/downloads and"
                " download 'Training images (Task 1 & 2)' and 'Validation images (all tasks)'."
            )


class ImageNet100(ImageNet1000):

    def __init__(
        self, *args, train_subset: Union[Tuple[np.array, np.array], str],
        test_subset: Union[Tuple[np.array, np.array], str], **kwargs
    ):
        super().__init__(self, *args, **kwargs)

        self.train_subset = train_subset
        self.test_subset = test_subset

    def init(self) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
        train = self._parse_subset(self.train_subset, train=True)
        test = self._parse_subset(self.test_subset, train=False)

        return train, test

    def _parse_subset(self,
                      subset: Union[Tuple[np.array, np.array], str],
                      train: bool = True) -> Tuple[np.array, np.array]:
        if isinstance(subset, str):
            x, y = [], []
            folder = self.train_folder if train else self.test_folder

            with open(subset) as f:
                for line in f:
                    split_line = line.split(" ")
                    path = "/".joint(split_line[0].strip().split("/")[1:])
                    x.append(os.path.join(folder, path))
                    y.append(int(split_line[1].strip()))

            x = np.concatenate(x)
            y = np.concatenate(y)
            return x, y
        return subset