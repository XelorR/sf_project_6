import os

import joblib
import pandas as pd
import numpy as np


def train_or_load(clf, X, y, filepath: str, complevel=9):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            clf = joblib.load(f)
    else:
        clf.fit(X, y)
        with open(filepath, "wb") as f:
            joblib.dump(clf, f, compress=complevel)
    return clf


def get_dumb_dummies(df: pd.DataFrame) -> pd.DataFrame:
    return pd.get_dummies(df, columns=df.select_dtypes("object").columns.tolist())


def mape(y_true, y_pred, **kwarg):
    return np.mean(np.abs((y_pred - y_true) / y_true))
