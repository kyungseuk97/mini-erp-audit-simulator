# 데이터 안내

이 프로젝트는 아래 Kaggle 데이터셋을 사용합니다.

**데이터셋**: [retail-store-sales-dirty-for-data-cleaning](https://www.kaggle.com/datasets/ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning)

## 전체 데이터 받는 방법

1. Kaggle 계정으로 로그인 후 위 링크에서 "Download" 클릭
   (또는 Kaggle CLI 사용: `kaggle datasets download -d ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning`)
2. 압축 해제 후 CSV 파일을 이 저장소의 `data/` 폴더 안에 넣기
   (저장소에는 라이선스 문제로 원본 전체 파일을 올리지 않습니다)

## 미리 보기용 샘플

`data/sample_retail_sales.csv` — 원본 앞부분 20건만 발췌한 샘플입니다.
코드 구조를 파악하거나 빠른 테스트용으로만 사용하세요. 실제 분석에는 전체 데이터를 받아서 사용해야 합니다.

## 컬럼 구조

| 컬럼 | 설명 |
|---|---|
| Transaction ID | 거래 고유번호 |
| Customer ID | 고객 고유번호 |
| Category | 상품 카테고리 (8종) |
| Item | 품목명 |
| Price Per Unit | 단가 |
| Quantity | 수량 |
| Total Spent | 총 금액 |
| Payment Method | 결제수단 (Cash / Credit Card / Digital Wallet) |
| Location | 판매 채널 (In-store / Online) |
| Transaction Date | 거래일자 |
| Discount Applied | 할인 적용 여부 |
