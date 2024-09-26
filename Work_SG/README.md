## ETL_PIPELINE

- Extract, Transform, Load / 데이터 수집, 정제, 저장

## 프로젝트 목표

- CP1
    - 기본적인 ETL 파이프라인 구축

- CP2
    - 

---

### Tech Stack

### Python

- Extract (추출)


- Transform (변환)


- Load (적재)

### AWS

---

### 3/27 업데이트

- cp1 프로젝트 코드 업로드

---

### 3/28 업데이트

- 데이터 선정
- cp2 api test 코드 업로드

---

### 4/2 업데이트

> EDA 진행
- 대상 : 데이터셋 중 201601 파일
- 내용
    - CMP_NM : 법인. 중요하지 않은 특성이므로 제거
    - DAN_NM : 단위. kg이 거의 대부분이므로 나머지 단위 제거
    - POJ_NM : 포장. 상자와 결측치가 대부분이므로 나머지 제거        
    - SIZE_NM : 크기. 결측치가 대부분이므로 삭제
    - LV_NM : 등급. 특 등급이 대부분이므로 특, 상, 보통, 등외 4가지로 정리
    - DANQ : 단위중량. 이상치와 취소된 거래 제거
    - QTY : 물량. 마이너스(-) 의 경우 취소된 거래이므로 제거
    - COST : 단가. 취소된 거래 제거
    - TOT_QTY : 총 물량. DANQ * QTY로 계산 가능
    - TOT_AMT : 총 금액. QTY * COST로 계산 가능
- 결과
    - csv 파일 : EDA 전 327mb -> EDA 후 213mb
    - json 파일 : EDA 전 1.4gb -> EDA 후 617mb

> 파일 압축 테스트
- json 원본 파일을 gzip, bz2, lzma 라이브러리로 각각 압축 후 압축률 비교
- json 원본 파일 : 617mb
  - gzip : 21.5mb, 96.62%
  - bz2 : 14.3mb, 97.69%
  - lzma : 18.1mb, 97.07%

> 발생한 오류와 해결
- pandas 라이브러리 사용 중 SettingWithCopyWarning 에러 발생 <br>
  코드가 작동은 했지만 지속적으로 에러 메시지 발생<br>
    - warning 라이브러리를 사용해서 해결
```python
import warnings
warnings.filterwarnings('ignore')
```
- EDA 진행 후 저장한 json 파일을 열 때 <br>
  invalid string length 에러 발생
    - orient 옵션 'table' -> 'index' 변경 후 해결
```python
convert_data.to_json('CP1/eda.json', orient='index', indent=4)
```

- EDA 진행 후 저장한 json 파일을 열 때 <br>
  데이터가 unicode 형태로 한글이 저장되는 현상 발생
    - pandas의 to_json 인자값 중 force_ascii=False 사용으로 해결
```python
convert_data.to_json('CP1/eda.json', orient='index', indent=4, force_ascii=False)
```

- json 데이터 파싱에러 발생 <br>
  json.decoder.JSONDecodeError: Expecting value: line 12 column 1 (char 22)
    - xmltodict 라이브러리 사용으로 해결
```python
import xmltodict
page = requests.get(url)
html = page.text

html_dict = xmltodict.parse(html)
```
