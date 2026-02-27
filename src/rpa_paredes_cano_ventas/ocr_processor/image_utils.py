from numpy import ndarray
from .helpers import get_roi_from_image, scale_image
from cv2 import cvtColor, COLOR_BGR2GRAY, threshold,THRESH_BINARY_INV
class ImageProcessor:
    """Clase dedicada exclusivamente a manipular la imagen."""
    
    @staticmethod
    def prepare_for_ocr(image: ndarray, coords: list[int], scale_factor: int = 3) -> ndarray:
        # 1. Recorte (ROI)
        roi = image if not any(coords) else get_roi_from_image(image, *coords)
        
        # 2. Escalado
        roi_resized = scale_image(roi, scale_factor)
        
        # 3. Conversión a escala de grises
        gray = cvtColor(roi_resized, COLOR_BGR2GRAY)
        
        # 4. Umbralización (Thresholding)
        # 
        _, thresh = threshold(gray, 140, 255, THRESH_BINARY_INV)
        
        return thresh