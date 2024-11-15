# PRND 사전 과제 프로젝트 실행 및 테스트 가이드

이 문서는 WantedLab 사전 과제를 docker 환경으로 실행하고 테스트하는 방법을 안내합니다.

## 요구 사항
- Python 3.8 이상
- FastAPI
- Docker 및 Docker Compose
- Postgresql
- SQLAlchemy
- Pydantic
- Alembic
- Uvicorn
- Nginx
<br/>

## 설치
1. **레포지토리 클론**
   
   ```bash
   git clone <레포지토리_URL>
   cd wanted_test
   ```
<br/>

## 실행
1. **Docker Compose로 실행**
   
   ```bash
   docker-compose up --build
   ```

   이 명령은 FastAPI 앱과 Postgresql, Nginx를 포함한 모든 서비스를 시작합니다.
   dockerfile과 docker_entrypoint.sh이 실행되면서 관련 라이브러리 설치와
   DB 마이그레이션, 초기 데이터 세팅 스크립트 실행이 완료됩니다.
<br/>

## 테스트
1. **Lint 실행**
   
   다음 명령으로 isort, black, flake8를 한 번에 실행할 수 있습니다.

   ```bash
   docker-compose exec web python lint.py
   ```
<br/>

2. **테스트 실행**
   
   다음 명령으로 pytest를 실행할 수 있습니다.

   ```bash
   docker-compose exec web pytest -v
   ```
<br/>

3. **API 테스트**

   3-1. **FastAPI Swagger UI 사용**

   이 프로젝트는 API 문서화를 위해 **FastAPI의 기본 Swagger UI**를 사용합니다. API 문서를 자동으로 생성하여 `/api/docs/` 경로에서 Swagger UI를 통해 확인할 수 있습니다.
   ```
   접속 url: http://localhost/api/docs/
   ```
   <br/>
<br/>

## 종료

   모든 서비스를 종료하려면 다음 명령을 실행합니다.
   ```bash
   docker-compose down
   ```
<br/>

## 문제 해결
1. **Docker 컨테이너 로그 확인**
   
   애플리케이션의 오류를 디버깅하려면 다음 명령으로 각 서비스의 로그를 확인할 수 있습니다.
   
   ```bash
   docker-compose logs -f web
   docker-compose logs -f db
   ```
<br/>

3. **DB 마이그레이션 실패 시**
   
   데이터베이스 마이그레이션에 문제가 발생하면 다음 명령으로 수동으로 마이그레이션을 실행할 수 있습니다.

   ```bash
   alembic revision --autogenerate -m "init"
   alembic upgrade head
   ```
<br/>

3. **초기 데이터 설정 (수동, 필요 시)**
   
   ```bash
   docker-compose exec web python app/scripts/init_data.py
   ```

