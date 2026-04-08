# MLOps OCR API Server 데모

FastAPI와 Tesseract OCR을 이용하여 이미지를 텍스트로 변환해주는 가벼운 서비스입니다.
이 프로젝트는 Docker 컨테이너로 구동할 것을 권장하며, Github Actions를 통한 CI/CD 환경이 구성되어 있습니다.

## 1. 시스템 의존성 (시스템 패키지)

이 프로젝트는 내부적으로 `pytesseract` 라이브러리를 사용하기 때문에, 실행 환경 내에 `tesseract-ocr` 바이너리가 필수로 설치되어 있어야 합니다. 
- (로컬에서 직접 실행할 경우) Ubuntu 환경: `sudo apt-get install tesseract-ocr tesseract-ocr-kor tesseract-ocr-eng`
- **Docker 사용 시**: `Dockerfile` 내에 시스템 패키지를 설치하는 스크립트가 포함되어 있으므로 **직접 설치할 필요가 없습니다!**

## 2. 프로젝트 로컬 실행 방법 (Docker 미사용)

Python 3.10 이상의 환경을 준비해주신 후, 아래 절차에 따릅니다.
(*주의: 로컬 시스템에 Tesseract-OCR가 미리 설치되어 있어야 합니다*)

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행 (uvicorn)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
서버가 올라가면 `http://localhost:8000` 에서 접속하실 수 있습니다.

## 3. Swagger(자동 문서화 API UI) 테스트 방법
FastAPI는 코드를 변경함에 따라 자동으로 Swagger API 문서를 생성합니다.
서버가 띄워진 상태에서 아래의 주소로 접속해 테스트가 가능합니다.

- **Swagger UI 접속 주소**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **테스트 방법**: 
  1. `/docs` 접속 후 화면에 보이는 `POST /ocr` 토글을 누릅니다.
  2. 우측의 **"Try it out"** 버튼을 클릭합니다.
  3. `file` 부분에 "Choose File"을 누르고 원하는 이미지 파일(png, jpg 등)을 하나 첨부합니다.
  4. 아래의 파란색 **"Execute"** 버튼을 누릅니다.
  5. 하단 쪽에 변환된 결과물(JSON 객체)이 짠 하고 나타납니다.

## 4. Github CI/CD 워크플로우
이 레포지토리는 Github을 통해 로컬 서버로 Docker 최신 이미지를 무중단(?) 배포하도록 설정되어 있습니다.

### 사전 요구 조건 (Secret 설정)
Github 저장소의 **Settings > Secrets and variables > Actions** 에 다음 두 개의 Secret을 추가해두어야 빌드가 동작합니다.
- `DOCKERHUB_USERNAME`: 본인의 도커 허브 아이디
- `DOCKERHUB_TOKEN`: 도커 허브에서 발급한 개인 토큰 (비밀번호보다 권장)

### Github Self-Hosted Runner 연결
Github 설정에서 본인의 컴퓨터를 Self-hosted runner로 등록해 두셨다면 (CD 단계 요구사항),
코드가 main에 푸쉬될 때 자동으로 도커 허브에서 방금 빌드된 이미지를 `pull` 하고, 기존 컨테이너를 중지, 새 이미지를 띄워줍니다.

### 도커 로컬 환경 수동 실행 (optional)
로컬에서 컨테이너를 확인해보고 싶다면:
```bash
docker build -t ocr-server .
docker run -p 8000:8000 ocr-server
```
