import pytesseract
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

async def process_image_to_text(image_bytes: bytes) -> tuple[str, list[str]]:
    """
    바이트 형태의 이미지 데이터를 입력받아 텍스트 스크립트와 라인 배열을 리턴합니다.
    """
    try:
        # 1. Pillow 라이브러리로 이미지 열기
        image = Image.open(io.BytesIO(image_bytes))
        
        # 2. pytesseract를 이용해 텍스트 추출 (한글 + 영문)
        # lang 파라미터는 설치된 언어팩(kor, eng)을 결합하여 지정합니다.
        extracted_text = pytesseract.image_to_string(image, lang='kor+eng')
        
        # 3. 추출된 텍스트를 정리하여 배열(lines) 분리
        # 좌우 공백을 제거하고 빈 줄은 제외합니다.
        lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
        
        return extracted_text.strip(), lines

    except Exception as e:
        # OCR 처리 중 발생하는 오류가 있다면 FastAPI에서 500에러를 반환할 수 있도록 예외를 던집니다.
        logger.error(f"OCR 처리 중 오류 발생: {str(e)}")
        raise e
