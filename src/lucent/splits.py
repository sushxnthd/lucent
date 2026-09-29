from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.model_selection import GroupShuffleSplit


@dataclass(frozen=True)
class GroupedSplit:
    """Indices for a train/test split with disjoint participant groups."""

    train: np.ndarray
    test: np.ndarray


def assert_disjoint_groups(
    groups: np.ndarray,
    train_idx: np.ndarray,
    test_idx: np.ndarray,
) -> None:
    """Raise if any participant/group appears in both train and test."""

    groups = np.asarray(groups)
    train_groups = set(groups[np.asarray(train_idx)].tolist())
    test_groups = set(groups[np.asarray(test_idx)].tolist())
    overlap = train_groups.intersection(test_groups)

    if overlap:
        preview = sorted(map(str, overlap))[:5]
        raise ValueError(f"group leakage detected: {preview}")


def grouped_train_test_split(
    groups: np.ndarray,
    *,
    test_size: float = 0.25,
    random_state: int = 42,
) -> GroupedSplit:
    """Create a participant-held-out split.

    Samples may repeat within a participant, but a participant can never occur
    in both partitions.
    """

    groups = np.asarray(groups)

    if groups.ndim != 1:
        raise ValueError("groups must be one-dimensional")
    if len(groups) < 2:
        raise ValueError("at least two observations are required")
    if len(np.unique(groups)) < 2:
        raise ValueError("at least two unique groups are required")

    index = np.arange(len(groups))
    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=test_size,
        random_state=random_state,
    )
    train_idx, test_idx = next(splitter.split(index, groups=groups))
    assert_disjoint_groups(groups, train_idx, test_idx)

    return GroupedSplit(train=train_idx, test=test_idx)
