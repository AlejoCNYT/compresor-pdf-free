import io
import os
import shutil
from PIL import Image

try:
    import pymupdf as fitz
except ImportError:
    import fitz


def pedir_parametros():
    print("=" * 58)
    print("   COMPRESOR PDF FREE - 100% LOCAL Y A COLOR")
    print('   "Ud no mas mande el tamano y le parcharemos free"')
    print("=" * 58)

    while True:
        entrada_kb = input("\nIngresa el tamano maximo deseado en KB (ej. 500): ").strip().replace(",", ".")
        try:
            tamano_kb = float(entrada_kb)
            if tamano_kb > 10:
                break
            print("Ingresa un valor mayor a 10 KB.")
        except ValueError:
            print("Valor no valido. Escribe solo el numero en KB (ej. 500).")

    carpeta = input("Nombre de la carpeta donde se guardaran (Enter para 'comprimidos_free'): ").strip()
    if not carpeta:
        carpeta = "comprimidos_free"

    for char in '<>:"/\\|?*':
        carpeta = carpeta.replace(char, "_")

    # Margen de seguridad de 3 KB para evitar redondeos hacia arriba en el Explorador
    limite_bytes = int((tamano_kb - 3) * 1024)
    return tamano_kb, limite_bytes, carpeta


def comprimir_archivo(ruta_archivo, limite_bytes):
    peso_original = os.path.getsize(ruta_archivo)
    if peso_original <= limite_bytes:
        return None, peso_original, None, None

    doc = fitz.open(ruta_archivo)
    ratio = limite_bytes / peso_original

    if ratio >= 0.5:
        dpi, calidad = 140, 75
    elif ratio >= 0.2:
        dpi, calidad = 115, 65
    else:
        dpi, calidad = 95, 55

    pdf_final = None
    dpi_usado, calidad_usada = dpi, calidad
    pdf_bytes = b""

    while dpi >= 20:
        nuevo_pdf = fitz.open()
        for pagina in doc:
            pix = pagina.get_pixmap(dpi=dpi, colorspace=fitz.csRGB)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=calidad, optimize=True)

            img_doc = fitz.open(stream=buf.getvalue(), filetype="jpeg")
            img_pdf = fitz.open("pdf", img_doc.convert_to_pdf())
            nuevo_pdf.insert_pdf(img_pdf)
            img_doc.close()
            img_pdf.close()

        pdf_bytes = nuevo_pdf.tobytes(garbage=4, deflate=True)
        nuevo_pdf.close()

        if len(pdf_bytes) <= limite_bytes:
            pdf_final = pdf_bytes
            dpi_usado, calidad_usada = dpi, calidad
            break

        if calidad > 35:
            calidad -= 10
        elif dpi > 45:
            dpi -= 15
            calidad = 55
        elif calidad > 15:
            calidad -= 10
        else:
            dpi -= 10
            calidad = 20

    doc.close()
    peso_resultado = len(pdf_final) if pdf_final else len(pdf_bytes)
    return pdf_final, peso_resultado, dpi_usado, calidad_usada


def main():
    tamano_kb, limite_bytes, carpeta_salida = pedir_parametros()
    pdfs = [f for f in os.listdir(".") if f.lower().endswith(".pdf")]

    if not pdfs:
        print("\nNo se encontraron archivos PDF en esta carpeta.")
        return

    os.makedirs(carpeta_salida, exist_ok=True)
    print(f"\nProcesando {len(pdfs)} documento(s) con limite de {tamano_kb:.0f} KB...\n")

    entregados = 0
    for archivo in pdfs:
        ruta_destino = os.path.join(carpeta_salida, archivo)
        pdf_bytes, peso_final, dpi, calidad = comprimir_archivo(archivo, limite_bytes)

        if pdf_bytes is None:
            shutil.copy2(archivo, ruta_destino)
            print(f"[OK - INTACTO]    {archivo}: {peso_final / 1024:.1f} KB (ya cumplia el limite)")
            entregados += 1
        elif len(pdf_bytes) <= limite_bytes:
            with open(ruta_destino, "wb") as f:
                f.write(pdf_bytes)
            print(f"[OK - COMPRIMIDO] {archivo}: {peso_final / 1024:.1f} KB (DPI={dpi}, Calidad={calidad}%)")
            entregados += 1
        else:
            print(
                f"[NO ENTREGADO]   {archivo}: minimo alcanzado {peso_final / 1024:.1f} KB "
                f"(excede {tamano_kb:.0f} KB; recorta paginas innecesarias e intentalo de nuevo)"
            )

    print(f"\nProceso terminado: {entregados}/{len(pdfs)} archivo(s) listos en '{carpeta_salida}'.")


if __name__ == "__main__":
    main()
