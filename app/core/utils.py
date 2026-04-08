from fastapi import UploadFile, HTTPException

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]

def validate_image_extension(file: UploadFile) -> None:
    """
    업로드된 파일이 허용된 형태의 이미지인지 검증하는 함수입니다.
    """
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 파일 형식입니다. (지원 형식: {', '.join(ALLOWED_IMAGE_TYPES)})"
        )
