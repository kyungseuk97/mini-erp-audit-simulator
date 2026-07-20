"""
Phase 1: 캐글 원본 데이터 구조 파악 + 완전성(결측치) 점검
데이터셋: ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning

주의: 이 데이터의 결측치는 '부정(fraud)'이 아니라 데이터 품질 이슈입니다.
      부정 데이터는 Phase 5에서 별도로 라벨을 붙여 직접 삽입합니다.
"""

import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """캐글 CSV 파일을 읽어서 DataFrame으로 반환한다."""
    return pd.read_csv(path)


def inspect_structure(df: pd.DataFrame) -> None:
    """데이터의 기본 구조(행/열 개수, 타입, 결측치)를 출력한다."""
    print("=== 행/열 개수 ===")
    print(df.shape)
    print("\n=== 컬럼별 데이터 타입 ===")
    print(df.dtypes)
    print("\n=== 결측치 개수 (컬럼별) ===")
    print(df.isna().sum())


def completeness_review(df: pd.DataFrame, check_cols: list[str], group_cols: list[str]) -> pd.DataFrame:
    """
    완전성(내부통제) 점검: check_cols 중 하나라도 비어있는 거래 비율을
    group_cols 기준으로 그룹핑해서 보여준다.
    -> 결측치가 특정 매장/결제수단/카테고리에 몰려있는지 확인하는 용도.
    """
    df = df.copy()
    df["is_missing"] = df[check_cols].isna().any(axis=1)

    print(f"=== 전체 결측 거래 비율 ===")
    print(f"{df['is_missing'].mean() * 100:.1f}% ({df['is_missing'].sum()}건 / {len(df)}건)\n")

    results = {}
    for col in group_cols:
        ratio = (df.groupby(col)["is_missing"].mean() * 100).round(1)
        results[col] = ratio
        print(f"=== {col} 별 결측 비율 ===")
        print(ratio, "\n")

    return results


if __name__ == "__main__":
    import sys

    # 기본값: data/ 폴더의 전체 데이터. 샘플로 빠르게 테스트하려면
    # python phase1_data_inspection.py data/sample_retail_sales.csv 처럼 인자로 경로를 넘기면 됨.
    DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/retail_sales.csv"

    df = load_data(DATA_PATH)
    inspect_structure(df)

    completeness_review(
        df,
        check_cols=["Item", "Price Per Unit", "Quantity", "Total Spent"],
        group_cols=["Location", "Payment Method", "Category"],
    )
