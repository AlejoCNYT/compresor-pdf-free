# Compresor PDF Free

> *"Ud no más mande el tamaño y le parcharemos free"*

Herramienta por consola para comprimir archivos PDF **100 % en local** (sin subir documentos personales, cédulas, registros civiles ni recibos a servidores externos), conservando el **color original (RGB)** y ajustando automáticamente la resolución hasta cumplir el límite exacto en KB exigido por portales universitarios o trámites en línea.

## Características
- **Privacidad total:** Todo el procesamiento ocurre en tu computador sin conexión a internet.
- **A color:** Mantiene sellos, firmas y fotografías en formato RGB.
- **Peso garantizado:** Calcula los parámetros necesarios y **no entrega** ningún archivo hasta que quede por debajo del límite configurado.
- **Sin pérdida innecesaria:** Si un PDF ya pesa menos del límite, lo copia intacto sin recomprimirlo.

## Requisitos
- **Python 3.10 o superior** instalado en Windows (asegúrate de marcar la casilla **Add python.exe to PATH** durante la instalación).
- Librerías `pymupdf` y `pillow` (incluidas en `requirements.txt`).

## Cómo usarlo paso a paso

1. **Ubica los archivos en una sola carpeta:**
   Coloca `compresor_pdf_free.py` y `requirements.txt` dentro de la misma carpeta donde tienes los archivos PDF que deseas comprimir.

2. **Abre PowerShell como Administrador desde la ruta de la carpeta:**
   - **En Windows 10:** Dentro de la carpeta en el Explorador de archivos, haz clic en el menú superior **Archivo -> Abrir Windows PowerShell -> Abrir Windows PowerShell como administrador**.
   - **En Windows 10 y 11:** Haz clic en la barra de direcciones del Explorador de archivos (donde se muestra la ruta de la carpeta), cópiala con `Ctrl + C`, abre el menú Inicio, busca **PowerShell**, haz clic en **Ejecutar como administrador** y entra a la carpeta ejecutando:
     ```powershell
     cd "PEGA_AQUI_LA_RUTA_COPIADA"
     ```

3. **Instala las dependencias (solo la primera vez):**
   ```powershell
   pip install -r requirements.txt
   ```
   *(Una vez instaladas las librerías, puedes desconectar el internet si deseas procesar tus documentos 100 % offline).*

4. **Ejecuta el compresor:**
   ```powershell
   python compresor_pdf_free.py
   ```

5. **Indica el tamaño y la carpeta de salida:**
   Escribe el peso máximo permitido en **KB** (por ejemplo, `500`) y el nombre de la carpeta donde se guardarán los documentos listos.

## Estructura del repositorio

```text
compresor-pdf-free/
├── compresor_pdf_free.py   # Script principal de compresión local a color
├── requirements.txt        # Dependencias de Python (pymupdf, pillow)
├── README.md               # Guía de instalación y uso paso a paso
├── .gitignore              # Evita subir PDFs personales por error al repo
└── LICENSE                 # Licencia MIT de uso libre
```

## Licencia
Este proyecto se distribuye bajo la licencia **MIT**. Úsalo, compártelo y adáptalo libremente.
