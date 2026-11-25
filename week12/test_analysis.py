from pathlib import Path

import pandas as pd

from analysis import 반별평균, 정제


DATA_DIR = Path(__file__).resolve().parent


def test_정제하면_100행이_남는다():
    df = 정제(pd.read_csv(DATA_DIR / "scores_2026.csv"))

    assert len(df) == 100


def test_정제후_반은_두종류만_남는다():
    df = 정제(pd.read_csv(DATA_DIR / "scores_2026.csv"))

    assert sorted(df["반"].unique()) == ["1반", "2반"]


def test_그룹별_점수합계가_전체합계와_같다():
    df = 정제(pd.read_csv(DATA_DIR / "scores_2026.csv"))

    assert df.groupby("반")["점수"].sum().sum() == df["점수"].sum()


def test_mini에서_1반_평균은_80점이다():
    df = 정제(pd.read_csv(DATA_DIR / "mini.csv"))

    assert 반별평균(df)["1반"] == 80.0