# Python 3.10 슬림 이미지를 베이스로 사용합니다.
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# tesseract-ocr 엔진과 언어팩(영어, 한국어) 설치
# 설치 후 불필요한 apt 캐시 지우기 (이미지 크기 최적화 목적)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-kor \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스코드 전체 복사
COPY . .

# FastAPI가 실행될 8000포트 개방 (문서화 목적)
EXPOSE 8000

# 컨테이너 실행 시 Uvicorn으로 FastAPI 앱 서버 시작
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
