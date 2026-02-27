from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol
import cv2
import pytesseract
from numpy import ndarray

# Interfaz para motores OCR
class OCREngine(ABC):
    @abstractmethod
    def extract(self, image: ndarray, lang: str, config: str) -> str:
        pass

# Implementación específica de Tesseract
class TesseractEngine(OCREngine):
    def __init__(self, executable_path: Path):
        pytesseract.pytesseract.tesseract_cmd = str(executable_path)

    def extract(self, image: ndarray, lang: str, config: str) -> str:
        return pytesseract.image_to_string(image, lang=lang, config=config)