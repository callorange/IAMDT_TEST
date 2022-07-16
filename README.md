# IAMDT_TEST
아이엠디티 코딩테스트를 위한 프로젝트 입니다.

## 구현 중점
스태프의 권한이나 그룹 구성 등 기본적으로 들어갔을 법한 기능에 고민이 많았으나 \
고민만 하다가 시간이 촉박해져서 **환자 상태 변화에만 집중하여 API를 구성**하기로 결정 하였습니다.

### 환자의 진료내역 묶음
각 환자의 상태는 최초 접수를 기준으로 관리 하여 히스토리를 각 접수 별로 그룹핑 할 수 있도록 구성 하였습니다.

### 주요사항
1. 접수
    * 진료, 퇴원 단계로 변경 가능.
2. 진료
    * 담당자 변경 알림
    * 진료, 진단, 처치, 결과 설명/상담 단계로 변경 가능
3. 진단
    * 담당자 변경 알림
    * 진료, 처치, 결과 설명/상담 단계로 변경 가능.
4. 처치
    * 담당자 변경 알림
    * 진료, 진단, 결과 설명/상담 단계로 변경 가능.
    * 환자 보호자에게 알림
5. 결과 설명/상담
    * 담당자 변경 알림
    * 접수, 수납, 퇴원 단계로 변경 가능.
    * 데스크 직원, 담당 수의사에게 알림
    * 결과 보고서 생성
6. 수납
    * 담당자 변경 알림
    * 수납 → 퇴원으로 단계 변경 가능.
    * 의약 처방전이 있는 경우
        - 처방전 인쇄.
        - 약품 재고에서 처방된 약품 개수 조절.
7. 퇴원
    * 보호자에게 진료 내역과 결과 발송.

### API 기능 예상
1. 고객 관리
2. 환자 관리
3. 스태프 관리
4. 약품 관리
5. 의료 서비스 접수 관리
   1. 진료 단계(접수/진료/진단/처치/상담/수납/퇴원) 내역
   2. 각 단계별 관리
   3. 처방전 관리
   4. 결과 보고서 관리
6. 약품 관리

### API 단계별 흐름
![flow](flow.png)


# 패키지 설치 및 실행
python 3.10 버전에서 개발 및 테스트 되었습니다.

## 사용 python 패키지
1. Django
2. DjangoRestFramework
3. DRF-Spectacular
4. Django-Filter
5. Django-silk
6. Django-extensions
7. black

## 필요 패키지 설치
### poetry
```shell
proejct_root> poetry install --no-dev
# 혹은
proejct_root> poetry install
```

### pip
```shell
proejct_root> pip install -r requirements.txt
# 혹은
proejct_root> pip install -r requirements_dev.txt
```

## 실행

### Secret Key 파일 생성
`Github`에서 `clone`한 경우 \
`ProjectRoot`에 `.secrets/local.json` 파일을 넣어야 합니다. \
혹은 환경변수 `DJANGO_SECRET_PATH`로 파일경로를 설정합니다.
```shell
# Windows
set DJANGO_SECRET_PATH=path/local.json
# Linux
export DJANGO_SECRET_PATH=path/local.json
```

### Unit Test
`proejct_root/iamdt/fixtures`에 테스트를 위한 초기 데이터가 있습니다. \
해당 데이터로 테스트를 진행합니다.
```shell
proejct_root/iamdt_django> python manage.py test
```

### 초기 데이터 세팅 
데이터가 없으므로 초기 데이터 세팅이 필요합니다. \
```shell
proejct_root/iamdt_django> python manage.py migrate # DB 마이그레이션
proejct_root/iamdt_django> python manage.py loaddata user customer patient medical_register medical_service medical_staff
```
1. SuperUser 권한
   - `admin`
2. Staff 권한
   - `doctor1`
   - `nurse1`
   - `employee1`
   - `dev1`
* 초기 유저의 비밀번호는 모두 `1234`입니다
### 실행 
```shell
proejct_root/iamdt_django> python manage.py runserver
# 별도 포트 지정
proejct_root/iamdt_django> python manage.py runserver 8000
```

### URL 접속

1. Index
   1. [index](http://localhost:8000/)
2. Django
   1. [Django Admin](http://localhost:8000/admin/) - 데이터 확인용
   2. [django silk](http://localhost:8000/silk/) - 쿼리 프로파일링(admin 페이지 로그인 필요)
3. API Document & Test
   1. [OAS Yaml](http://localhost:8000/api/doc/scheme) - OAS 3.0 YAML 파일
   2. [swagger ui](http://localhost:8000/api/doc/swagger) - Swagger UI. Test 가능
   3. [redoc ui](http://localhost:8000/api/doc/redoc) - Redoc Ui. Test 기능 X

## 구현한 API 구조

1. 인증
   * 유저로그인 /auth/login
   * 유저로그아웃 /auth/logout
2. 스태프 
   * 스태프검색  /staff
   * 스태프등록  /staff
   * 스태프정보  /staff/\<id:int>
   * 스태프수정  /staff/\<id:int>
   * 스태프스케쥴  /staff/\<int:id>/schedules
3. 고객
   * 고객검색  /customers
   * 고객등록  /customers
   * 고객정보  /customers/\<id:int>
   * 고객수정  /customers/\<id:int>
4. 환자
   * 환자검색  /patients
   * 환자등록  /patients
   * 환자정보  /patients/\<id:int>
   * 환자수정  /patients/\<id:int>
   * 환자진료내역  /patients/\<id:int>/services
5. 진료내역
   * 진료검색  /services
   * 진료등록  /services
   * 진료정보  /services/\<int:id>
