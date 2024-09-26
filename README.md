# ETL_Pipeline Project

- Extract(추출), Transform(변환), Load(적재)의 축약어인 ETL은 백엔드에서 데이터 수집, 정제, 저장의 한 과정을 말합니다.
- 이 프로젝트는 ETL 파이프라인을 직접 만들어보고, ETL에 대한 인사이트를 얻기 위해 기획되었습니다.

# 프로젝트 목표

- ETL 파이프라인을 구축해본다.
    - API 서비스에서 데이터를 추출(Extract), 변환(Transform), 압축(Compress)하기 위한 파이썬 모듈을 적용해본다.
    - 배포할 준비가 된 데이터를 AWS 서비스에 적재(Load)해본다.
    - 적재된 데이터를 요청(Request)해서 데이터가 올바르게 전달(Response)되는지 확인해본다.

## Tech Stack

---

### Python

> Extract (추출)
> 
- APScheduler 모듈을 사용한 데이터 요청 일정 시간 간격마다 수집
- requests 모듈을 사용한 데이터 받아오기

> Transform (변환)
> 
- cryptography 모듈을 사용한 암호화된 데이터 복호화
- b64uuid 모듈을 사용한 아이디 문자열 축소
- datetime 모듈을 사용한 timestamp 데이터를 연/월/일/시 시간 데이터로 변환
- gzip 또는 zlib 모듈을 사용한 데이터 압축 수행

> Load (적재)
> 
- boto3 모듈을 사용한 aws s3 서비스에 데이터 적재

### AWS

> 인증
> 
- IAM 서비스를 사용해서 aws 접근 제어

> 클라우드 가상pc
> 
- EC2 서비스를 사용해서 aws 서비스 안에서 python 스케줄링 코드 작동

> 데이터 적재
> 
- S3 서비스를 사용해서 aws 서비스에 추출, 변환한 데이터 적재

---

### 개발 로그
[여기로](doc/LOG.md)