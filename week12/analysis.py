import pandas as pd

df = pd.read_csv("scores_2026_cp949.csv", encoding="cp949")

print(df.shape)
print(df["점수"].isna().sum())
print(df.duplicated().sum())
print(df["반"].unique())
print(df["과목"].unique())
print(df["점수"].describe())

'''
[역할]  너는 파이썬 데이터 처리를 돕는 조교다.

[목표]  아래 명세대로 CSV를 정제하는 함수 정제(df)를 만들어라.

[데이터]
  파일: scores_2026.csv, 114행 5열 (학번 이름 반 과목 점수)
  점수는 0 이상 100 이하의 정수여야 한다.
  반과 과목 값의 앞뒤에 공백이 섞여 있다.

[처리 규칙]  ← 명세서 ③④⑤ 칸 + 데이터 특성을 옮깁니다
  1) 점수가 비어 있는 행은 삭제한다.
  2) 모든 열이 완전히 같은 행은 하나만 남긴다.
  3) 반과 과목의 앞뒤 공백을 제거한다.
  4) 점수가 0~100 밖인 행은 삭제한다.

[제약]  pandas만 사용. 각 단계 뒤 남은 행 수를 print 할 것.
'''
def 정제(df):
    # 1) 점수가 비어 있는 행 삭제
    df = df.dropna(subset=["점수"])
    print(f"After dropping rows with NaN scores: {df.shape[0]} rows remaining.")

    # 2) 모든 열이 완전히 같은 행은 하나만 남긴다.
    df = df.drop_duplicates()
    print(f"After dropping duplicate rows: {df.shape[0]} rows remaining.")

    # 3) 반과 과목의 앞뒤 공백 제거
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print(f"After stripping whitespace from '반' and '과목': {df.shape[0]} rows remaining.")

    # 4) 점수가 0~100 밖인 행 삭제
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print(f"After filtering scores outside 0-100 range: {df.shape[0]} rows remaining.")

    return df

df_clean = 정제(df.copy())

print("최종 행·열:", df_clean.shape)
print("반 종류:", sorted(df_clean["반"].unique()))
print("과목 종류:", sorted(df_clean["과목"].unique()))

math_df = df_clean[df_clean["과목"] == "수학"]
print("수학 행 수:", len(math_df))

challenge_df = df_clean[
    (df_clean["반"] == "1반") & (df_clean["점수"] >= 90)
]
print("1반이면서 90점 이상:", len(challenge_df))

print(df_clean.groupby("반")["점수"].mean().round(2))
print(df_clean.groupby(["과목", "반"])["점수"].mean().round(2))

def 반별평균(df):
    통계표 = df.groupby("반")["점수"].agg(
        ["count", "mean", "median", "max"]
    ).round(2)
    print(통계표)
    return 통계표["mean"]

평균값 = 반별평균(df_clean)
print("평균값:", 평균값)

# 그룹별 합계와 전체 합계 비교
print(df_clean.groupby("반")["점수"].sum().sum())
print(df_clean["점수"].sum())

# 그룹별 행 수와 전체 행 수 비교
print(df_clean.groupby("반")["점수"].count().sum())
print(len(df_clean))

# 1반 수학 평균을 직접 검산
sample = df_clean[
    (df_clean["반"] == "1반") & (df_clean["과목"] == "수학")
]
print(sorted(sample["점수"].tolist()))
print(sample["점수"].sum() / len(sample))