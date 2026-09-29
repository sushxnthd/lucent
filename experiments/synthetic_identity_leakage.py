"""Synthetic demonstration of identity leakage.

The generated data contain:
1. a transient "state" feature that genuinely relates to the target; and
2. a stable participant embedding paired with a participant-specific bias.

When observations from the same participant appear in both train and test,
a flexible model can exploit identity and look much better than it really
generalizes. Holding out entire participants exposes the shortcut.

This is a didactic experiment only. It is not a Lucent performance result.
"""

from __future__ import annotations

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from lucent.metrics import regression_report
from lucent.splits import grouped_train_test_split


SEED = 7


def make_synthetic_dataset(
    *,
    n_participants: int = 120,
    visits_per_participant: int = 10,
    identity_dims: int = 8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(SEED)

    identity = rng.normal(size=(n_participants, identity_dims))
    participant_bias = rng.normal(0.0, 1.5, size=n_participants)

    features: list[np.ndarray] = []
    targets: list[float] = []
    groups: list[int] = []

    for participant in range(n_participants):
        for _ in range(visits_per_participant):
            latent_state = rng.normal()
            measured_visual_state = latent_state + rng.normal(0.0, 0.35)

            identity_features = (
                identity[participant]
                + rng.normal(0.0, 0.05, size=identity_dims)
            )

            x = np.concatenate(
                [identity_features, np.array([measured_visual_state])]
            )
            y = (
                0.8 * latent_state
                + participant_bias[participant]
                + rng.normal(0.0, 0.25)
            )

            features.append(x)
            targets.append(float(y))
            groups.append(participant)

    return (
        np.asarray(features),
        np.asarray(targets),
        np.asarray(groups),
    )


def model() -> object:
    return make_pipeline(
        StandardScaler(),
        KNeighborsRegressor(n_neighbors=5, weights="distance"),
    )


def evaluate(
    x: np.ndarray,
    y: np.ndarray,
    train_idx: np.ndarray,
    test_idx: np.ndarray,
):
    estimator = model()
    estimator.fit(x[train_idx], y[train_idx])
    prediction = estimator.predict(x[test_idx])
    return regression_report(y[test_idx], prediction)


def main() -> None:
    x, y, groups = make_synthetic_dataset()
    index = np.arange(len(y))

    random_train, random_test = train_test_split(
        index,
        test_size=0.25,
        random_state=SEED,
    )

    grouped = grouped_train_test_split(
        groups,
        test_size=0.25,
        random_state=SEED,
    )

    random_report = evaluate(x, y, random_train, random_test)
    grouped_report = evaluate(x, y, grouped.train, grouped.test)

    print("Synthetic identity-leakage demonstration")
    print("=" * 42)
    print(
        "Random clip split:       "
        f"R²={random_report.r2: .3f}  MAE={random_report.mae: .3f}"
    )
    print(
        "Participant-held-out:    "
        f"R²={grouped_report.r2: .3f}  MAE={grouped_report.mae: .3f}"
    )
    print()
    print(
        "Interpretation: the random split lets the model reuse stable identity "
        "information from people it has already seen. The grouped split removes "
        "that shortcut."
    )


if __name__ == "__main__":
    main()
