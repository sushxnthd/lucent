import numpy as np
import pytest

from lucent.splits import assert_disjoint_groups, grouped_train_test_split


def test_grouped_split_has_no_participant_overlap():
    groups = np.repeat(np.arange(20), 5)
    split = grouped_train_test_split(groups, test_size=0.25, random_state=1)

    train_groups = set(groups[split.train])
    test_groups = set(groups[split.test])

    assert train_groups.isdisjoint(test_groups)


def test_assert_disjoint_groups_rejects_leakage():
    groups = np.array([0, 0, 1, 1])
    train = np.array([0, 2])
    test = np.array([1, 3])

    with pytest.raises(ValueError, match="group leakage"):
        assert_disjoint_groups(groups, train, test)
