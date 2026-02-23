import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from loguru import logger


class VasicontLauncher:
    """Modo 3: Copiar carpeta solo una vez y reutilizar siempre."""

    def __init__(self, exe_path: Path) -> None:
        self.exe_path = exe_path
        self.local_dir = Path(tempfile.gettempdir()) / "vasicont_temp"
        self.flag_file = self.local_dir / "ready.flag"

    def _prepare_local_copy(self) -> Path:
        """
        Copia TODO el directorio a local SOLO la primera vez.
        Después solo retorna la copia local sin copiar nada.
        """
        exe_str = str(self.exe_path)
        is_unc_path = exe_str.startswith("\\\\") or exe_str.startswith("\\\\?\\UNC")

        # Si NO es ruta UNC → usar directo
        if not is_unc_path:
            logger.debug("Ruta local detectada, no se requiere copia.")
            print(f"Ejecutable local existente: {self.exe_path}")
            return self.exe_path

        # Si YA está copiado → NO copiar de nuevo
        if self.flag_file.exists():
            copied_exe = self.local_dir / self.exe_path.name
            logger.debug("Copia local ya existente, reutilizando.")
            print(f"Usando copia local existente: {copied_exe}")
            return copied_exe

        # Si NO está copiado, copiar solo una vez
        logger.info("Primera ejecución: copiando carpeta completa a local...")
        print("Copiando carpeta completa a local...")

        src_folder = self.exe_path.parent
        self.local_dir.mkdir(exist_ok=True)

        # Copiar toda la carpeta pero solo una vez
        for item in src_folder.iterdir():
            dest = self.local_dir / item.name
            try:
                if item.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)
            except Exception as e:
                logger.error(f"Error copiando {item} → {dest}: {e}")
                raise

        # Crear "flag" para no copiar nunca más
        self.flag_file.write_text("ready")

        local_exe = self.local_dir / self.exe_path.name
        logger.success(f"Carpeta copiada una sola vez. Ejecutable listo: {local_exe}")
        print(f"Carpeta copiada una sola vez. Ejecutable listo: {local_exe}")

        return local_exe

    def open(self, wait_seconds: int = 5) -> subprocess.Popen:
        """Abre la aplicación usando la copia local (o la ruta original si no era UNC)."""
        try:
            exe_to_run = self._prepare_local_copy()
            exe_str = str(exe_to_run)

            logger.info(f"Abrriendo aplicación: {exe_str}")
            print(f"Abriendo aplicación: {exe_str}")

            process = subprocess.Popen(
                [exe_str],
                shell=False,
                cwd=str(exe_to_run.parent),
            )

            logger.info("Esperando para verificar si la app sigue abierta...")
            time.sleep(wait_seconds)

            if process.poll() is None:
                logger.success("Aplicación iniciada correctamente.")
                print(f"Aplicación ejecutándose correctamente desde: {exe_str}")
            else:
                logger.warning(f"La aplicación se cerró. Código: {process.returncode}")
                print(f"La aplicación se cerró. Código: {process.returncode}")

            return process

        except FileNotFoundError:
            logger.error(f"No se encontró el ejecutable: {self.exe_path}")
            raise
        except Exception as e:
            logger.exception(f"Error al iniciar la app: {e}")
            raise
