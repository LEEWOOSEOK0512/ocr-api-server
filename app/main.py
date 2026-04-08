from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

# FastAPI 애플리케이션 초기화
app = FastAPI(
    title="MLOps OCR API Server",
    description="FastAPI와 Tesseract를 이용한 초간단 OCR 서버 데모입니다.",
    version="1.0.0"
)

# CORS 미들웨어 허용 (필요시 도메인 제한 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router)
