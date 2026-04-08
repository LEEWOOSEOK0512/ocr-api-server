from pydantic import BaseModel
from typing import List

class OCRResponse(BaseModel):
    extracted_text: str
    lines: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "extracted_text": "Hello World\nThis is a test",
                "lines": [
                    "Hello World",
                    "This is a test"
                ]
            }
        }
