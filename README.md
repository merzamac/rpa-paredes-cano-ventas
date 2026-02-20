# rpa-paredes-cano-ventas
# 🤖 Bot de Procesamiento Masivo e Integración: Aconsys & Importación

## 📄 Descripción del Proyecto
Este repositorio contiene un motor de automatización (RPA/ETL) diseñado para la orquestación de datos a gran escala entre archivos locales y plataformas empresariales (**Plataforma de Importación** y **Aconsys**). 

El sistema está optimizado para procesar archivos que superan los **300,000 registros**, utilizando técnicas de **Streaming y Chunking** para garantizar un consumo de memoria RAM eficiente y constante, evitando desbordamientos durante el ciclo de vida del dato.

---

## 🛠 Arquitectura y Patrones de Diseño
El proyecto implementa un diseño de **Service Layer Orchestrator**, separando la lógica de negocio de la interacción con las interfaces de usuario o APIs.

### Componentes Clave:
* **ETL Engine (Extract, Transform, Load):** Lectura fragmentada de archivos de entrada, limpieza de ruido de datos y validación de reglas de negocio.
* **Synchronizer Service:** Encargado de la comunicación bidireccional y carga de archivos en la Plataforma de Importación.
* **Reconciliation Module (Aconsys):** Lógica avanzada de comparación entre los resultados de importación y los reportes de Aconsys para la detección de **Series Nuevas**.
* **Auto-Registration Logic:** Registro automatizado de discrepancias en ambas plataformas para asegurar la integridad del ecosistema.

---

## ⚙️ Flujo de Operación (Workflow)

1.  **Ingesta de Datos:** Obtención de archivos fuente y procesamiento por bloques (**Chunks de 10k a 50k filas**).
2.  **Normalización:** Limpieza, validación de columnas y generación de archivos CSV masivos compatibles.
3.  **Carga Masiva:** Inyección de datos en la Plataforma de Importación y monitoreo de resultados.
4.  **Análisis de Resultados:**
    * **Escenario A:** Sin detalles -> El proceso finaliza con éxito.
    * **Escenario B:** Con detalles -> Se activa el **Protocolo de Conciliación**.
5.  **Conciliación Aconsys:** Descarga de reportes desde Aconsys, extracción de atributos y comparación cruzada.
6.  **Sincronización:** Registro de nuevas series detectadas tanto en Aconsys como en la Plataforma de Importación.

---

## 🚀 Capacidades de Alto Rendimiento
* **Escalabilidad:** Procesamiento de **>300k registros** sin degradación de performance mediante iteradores y generadores de Python.
* **Resiliencia:** Manejo robusto de excepciones para evitar interrupciones por tiempos de respuesta de las plataformas externas.
* **Bajo Footprint de Memoria:** Diseñado para ejecutarse en entornos con recursos limitados gracias al procesamiento por lotes.

---

## 📂 Requisitos Técnicos
* **Lenguaje:** Python 3.10+
* **Librerías Core:** * `pandas`: Para la manipulación eficiente de grandes dataframes.
    * `python-dotenv`: Manejo de variables de entorno y credenciales.
    * `logging`: Trazabilidad detallada del proceso.

---

## 🔧 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)
    ```
2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configurar variables de entorno (.env):**
    ```env
    ACONSYS_USER=tu_usuario
    IMPORT_PLATFORM_URL=[https://api.ejemplo.com](https://api.ejemplo.com)
    CHUNK_SIZE=50000
    ```
4.  **Ejecutar el bot:**
    ```bash
    python main.py
    ```

---
> **Nota de Seguridad:** Asegúrate de no subir el archivo `.env` al repositorio público. Utiliza el archivo `.env.example` proporcionado como plantilla.
