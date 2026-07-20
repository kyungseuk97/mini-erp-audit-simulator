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

## 캐글 원본 vs 회계 전표에 필요한 컬럼 (Phase 1 정리)

| 캐글 원본 컬럼 | 있음/없음 | 회계 전표 관점 설명 |
|---|---|---|
| Transaction ID | 있음 | 전표번호로 그대로 활용 가능 |
| Customer ID | 있음 | 거래처 코드로 활용 |
| Category, Item | 있음 | 계정과목 자체는 아니고, 매출 세부계정 분류용 |
| Price Per Unit, Quantity, Total Spent | 있음 | 금액 산정용 |
| Payment Method | 있음 | 계정과목(차변) 결정용 — 매핑표(`data/계정과목_매핑_예시.xlsx`) 참고 |
| Transaction Date | 있음 | 거래일자로 활용 가능 |
| 전표번호(고유 채번 규칙) | 없음 | Transaction ID를 그대로 쓸지, 별도 규칙으로 채번할지 결정 필요 |
| 계정과목 코드 / 차대변 구분 | 없음 | 원본엔 "매출/매입" 구분조차 없음(이 데이터는 전부 매출 거래). Payment Method 매핑표로 새로 생성 |
| 기안자/승인자(Approval) | 없음 | 통제 필드 — Phase 2에서 임의 생성 필요 |
| 전표입력일자(Posting Date) | 없음 | 원본엔 Transaction Date 하나뿐. cut-off 테스트를 위해 별도로 posting date 생성 필요 |
| 취소/정정 여부(Void Flag) | 없음 | 없음, 필요시 Phase 2에서 생성 |

**결론**: 이 데이터는 매출 거래만 있는 원시 판매기록이라, 회계 전표가 되려면 계정과목/차대변, 승인자, Posting Date, Void Flag 4가지를 `transform_to_voucher()` 함수(Phase 2)에서 새로 붙여야 합니다.
