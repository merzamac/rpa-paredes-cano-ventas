
import matplotlib.pyplot as plt  # type: ignore
from numpy import ndarray
from cv2 import cvtColor,COLOR_RGB2BGR,resize,INTER_CUBIC,COLOR_BGR2RGB
from numpy import array, ndarray
from PIL.Image import Image
from PIL.ImageGrab import grab
from uiautomation import Control, Rect


def take_screenshot(control: Control) -> Image:
    coords: Rect = control.BoundingRectangle
    img: Image = grab(bbox=(coords.left, coords.top, coords.right, coords.bottom))
    return img

def img_to_ndarry(img: Image) -> ndarray:
    img_cv: ndarray = cvtColor(array(img), COLOR_RGB2BGR)
    return img_cv


def get_roi_from_image(img: ndarray, top=0, right=0, bottom=0, left=0):
    height, width, _ = img.shape
    return img[height - top : height - bottom, width - right : width - left]


def scale_image(img: ndarray, scale_factor: int) -> ndarray:
    """
    Toma la Región de Interés (ROI) y la amplía 3 veces su tamaño original en ambas dimensiones.
    Usa interpolación bicúbica para mantener una buena calidad en la imagen ampliada.
    """
    return resize(
        img,
        None,
        fx=scale_factor,
        fy=scale_factor,
        interpolation=INTER_CUBIC,
    )


def show(img: ndarray, roi_resized: ndarray, gray: ndarray, thresh: ndarray) -> None:
    # Mostrar imágenes en diferentes etapas
    _, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(cvtColor(img, COLOR_BGR2RGB))
    axes[0].set_title("Imagen Original")
    axes[0].axis("off")

    axes[1].imshow(cvtColor(roi_resized, COLOR_BGR2RGB))
    axes[1].set_title("ROI Redimensionada")
    axes[1].axis("off")

    axes[2].imshow(gray, cmap="gray")
    axes[2].set_title("Escala de Grises")
    axes[2].axis("off")

    axes[3].imshow(thresh, cmap="gray")
    axes[3].set_title("Umbralizado")
    axes[3].axis("off")

    plt.show()