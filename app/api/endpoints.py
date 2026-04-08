from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.ocr import OCRResponse
from app.services.ocr_service import process_image_to_text
from app.core.utils import validate_image_extension

router = APIRouter()

@router.get("/health", tags=["System"])
async def health_check():
    """
    서버의 정상 구동 여부를 확인하는 헬스 체크 엔드포인트입니다.
    """
    return {"status": "ok", "message": "MLOps OCR API Server is running happily!"}


@router.post("/ocr", response_model=OCRResponse, tags=["ML Models"])
async def run_ocr(file: UploadFile = File(..., description="텍스트를 추출할 이미지 파일 (png, jpeg, webp)")):
    """
    사용자가 업로드한 이미지 파일(multipart/form-data)을 받아서
    내부 텍스트를 추출해 JSON 결과로 반환합니다.
    """
    # 1. 파일 확장자/MIME 검증 (이미지가 아닌 경우 400 에러 처리)
    validate_image_extension(file)

    try:
        # 2. 비동기 환경에서도 안전하게 파일 전체 읽기
        image_bytes = await file.read()
        
        # 3. 비즈니스 로직(OCR) 서비스 호출
        extracted_text, lines = await process_image_to_text(image_bytes)
        
        # 4. 결과값 반환
        return OCRResponse(extracted_text=extracted_text, lines=lines)
        
    except Exception as e:
        # OCR 분석 중 오류 발생 시 500 응답
        raise HTTPException(status_code=500, detail=f"이미지 분석 중 문제가 발생했습니다: {str(e)}")
