"""
Phase 3: 파이썬에서 만든 분개 데이터를 노션 Journal Entry DB로 업로드한다.

주의: 노션 API는 초당 약 3건 정도의 요청만 처리 가능하다.
전체(약 4만 줄)를 다 올리면 몇 시간이 걸리므로, 기본적으로 일부(limit)만 올린다.
전체 데이터는 계속 파이썬 쪽에 남아서 GL/TB/FS, 감사 절차 계산에 쓰인다.
"""

import os
import time
import requests
import pandas as pd


def load_credentials(path: str = "Notion.txt") -> dict:
    """
    'KEY=VALUE' 형식으로 한 줄씩 적힌 텍스트 파일을 읽어서 딕셔너리로 반환한다.
    예:
        NOTION_API_KEY=ntn_xxxx
        NOTION_JE_DATABASE_ID=xxxx
    """
    creds = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            creds[key.strip()] = value.strip()
    return creds


creds = load_credentials("Notion.txt")
NOTION_API_KEY = creds["NOTION_API_KEY"]
DATABASE_ID = creds["NOTION_JE_DATABASE_ID"]

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def je_row_to_notion_properties(row: pd.Series) -> dict:
    """분개 DataFrame의 한 행을 노션 페이지 속성(properties) 형식으로 변환한다."""
    return {
        "Voucher No": {"title": [{"text": {"content": str(row["Voucher No"])}}]},
        "Prepared By": {"select": {"name": str(row["Prepared By"])}},
        "Approved By": {"select": {"name": str(row["Approved By"])}},
        "Posting Date": {"date": {"start": pd.Timestamp(row["Posting Date"]).strftime("%Y-%m-%d")}},
        "JE Type": {"select": {"name": str(row["JE Type"])}},
        "Account": {"rich_text": [{"text": {"content": str(row["Account"])}}]},
        "Debit": {"number": float(row["Debit"])},
        "Credit": {"number": float(row["Credit"])},
    }


def export_to_notion(je: pd.DataFrame, limit: int = 100, delay: float = 0.35) -> None:
    """
    분개 DataFrame을 노션 DB에 한 줄씩 업로드한다.
    limit: 노션에 올릴 최대 줄 수 (속도 제한 때문에 기본값을 작게 둠)
    delay: 각 요청 사이 대기 시간(초). 너무 빠르면 노션이 요청을 거부(429 에러)할 수 있음.
    """
    subset = je.head(limit)
    success, failed = 0, 0

    for _, row in subset.iterrows():
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": je_row_to_notion_properties(row),
        }
        response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)

        if response.status_code == 200:
            success += 1
        else:
            failed += 1
            print(f"실패: {row['Voucher No']} / {row['Account']} -> {response.status_code} {response.text[:200]}")

        time.sleep(delay)

    print(f"\n완료: 성공 {success}건 / 실패 {failed}건 (전체 {len(je)}건 중 {limit}건만 시도)")


if __name__ == "__main__":
    # phase2_journal_entries.py의 함수들을 그대로 가져와서 분개 데이터를 만든 뒤 업로드
    from phase2_journal_entries import (
        load_payment_rules, load_category_rules, transform_to_voucher, generate_journal_entries
    )

    DATA_PATH = "data/retail_sales.csv"
    RULES_PATH = "data/Je_rules_매핑_통합본.xlsx"

    df = pd.read_csv(DATA_PATH)
    payment_rules = load_payment_rules(RULES_PATH)
    category_rules = load_category_rules(RULES_PATH)
    voucher = transform_to_voucher(df)
    je = generate_journal_entries(voucher, payment_rules, category_rules)

    export_to_notion(je, limit=20)  # 처음엔 20건만 테스트
