# <U>ETL Pipeline CP1 </U>
----

## ETL 파이프라인 구축

**API 요청으로 암호화된 데이터를 추출하여, 적절한 처리를 진행한 뒤 로컬 및 AWS S3 에 적재한다.**

**일정 주기로 Pipeline이 실행되도록 Scheduling 한다.**
### ➡️ API 요청 데이터 추출 및 처리 
### ➡️ 로컬 적재 
### ➡️ Data Partitioning 및 Data Compression 
### ➡️ 압축된 로그 AWS S3 적재 
### ➡️ 스케쥴링

----
![ETL_CP1_Architecture](https://user-images.githubusercontent.com/97868775/226523848-0809cc15-a626-405e-b6b1-77130b96be90.jpg)

----
----

### ➡️ API 요청 데이터 추출 및 처리 ➡️ 로컬 적재

#### ◼️ 주어진 url 과 key 를 이용한 api 요청 로그데이터 추출 (100 개)

#### ◼️ 추출된 log 데이터를 로컬에서 처리
**1. 중복 검사**
+ 한번 처리했던 log는 제외하고 새로 받은 log만 처리 진행
+ recordId 이용하여 중복 검사
+ 모든 로그는 로컬에 적재(.json)
+ 새로 받는 log가 없으면, 이후 과정 진행하지 않음

**2. 암호화된 log 복호화**

**3. user_id : 64자로 구성된 user_id 를 44자로 변환**
+ b64uuid 모듈 사용

**4. method : HTTP method 를 숫자로 변환**
* method 를 한자리 숫자로 변환
* 새로운 method 등장 시, 숫자 할당 후 변환

**5. url : method 와 마찬가지로 변환**
* url 의 product number 을 사용하여 변환
* product number 없을 시 0 할당
* 새로운 url/product_number 등장 시, 해당 product number 할당 후 변환

**6. inDate : 표시 형식 변환**
* ```2022-12-05T12:14:00.179Z``` 의 형식을 ```221205121400179```의 형식으로 변환
* Data Partitioning 을 위한 inDate 항목 log에 추가

**7. 암호화**

**8. 더이상 의미없는 항목 삭제**
* ```recordId```, ```ArrivalTimeStamp``` 삭제

#### ◼️ 로컬에 모든 log 적재
**1. 처리되기 전 log 적재 (.json)**

**2. 처리된 후 log 적재 (.json)**

----

### ➡️ Data Partitioning 및 Data Compression

#### ◼️ Data Partitioning

**1. inDate 의 '년도/월/일/시간' 으로 처리된 log를 분류**

#### ◼️ Data Compression
**1. 분류된 log 를 Data Compression (압축 알고리즘 적용)**
* ```gzip``` 라이브러리 사용
* 파일명은 inDate의 '년도+월+일+시간' 으로 설정
* 이미 해당 시간대의 압축 파일이 있으면, 그 파일에 추가

**2. 모든 압축파일은 로컬에 적재**

----

### ➡️ 압축된 로그 AWS S3 적재

#### ◼️ 압축 파일을 로컬에 적재함과 동시에 AWS S3 에도 적재
**1. AWS S3 bucket 생성**
* 모든 ACCESS KEY 는 ```dotenv``` 라이브러리 사용하여 보안

**2. 해당 bucket에 압축파일 적재**
* Data Partitioning 된 디렉토리 명은 각각 '년도' '월' '일' '시간' 으로 설정

----

### ➡️ 스케쥴링

#### ◼️ 모든 과정을 일정 주기마다 실행되도록 Scheduling
**1. 3분 주기로 scheduling**
* ```APScheduler``` 사용