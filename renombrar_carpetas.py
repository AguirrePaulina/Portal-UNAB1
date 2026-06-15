"""
renombrar_carpetas.py
Se Ejecuta UNA SOLA VEZ en PythonAnywhere (consola Bash):
  python3 renombrar_carpetas.py

Renombra carpetas dentro de static/materiales/ eliminando tildes y comas,
para que coincidan con las rutas que genera el frontend.
"""
import os, unicodedata, re, shutil

def normalizar(nombre):
    nfd = unicodedata.normalize("NFD", nombre)
    sin_tildes = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    s = sin_tildes.upper().strip()
    s = re.sub(r"[,.']+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


MAT_DIR = os.path.join(os.path.dirname(__file__), "static", "materiales")

if not os.path.isdir(MAT_DIR):
    print(f"ERROR: No existe el directorio {MAT_DIR}")
    exit(1)

renombrados = 0
for entry in os.listdir(MAT_DIR):
    ruta_orig = os.path.join(MAT_DIR, entry)
    if not os.path.isdir(ruta_orig):
        continue
    nuevo = normalizar(entry)
    if nuevo == entry:
        print(f"  OK (sin cambios): {entry}")
        continue
    ruta_nueva = os.path.join(MAT_DIR, nuevo)
    if os.path.exists(ruta_nueva):
        # Ya existe destino: mover archivos dentro
        print(f"  MERGE: {entry!r} -> {nuevo!r} (destino ya existe, moviendo archivos)")
        for f in os.listdir(ruta_orig):
            src = os.path.join(ruta_orig, f)
            dst = os.path.join(ruta_nueva, f)
            if not os.path.exists(dst):
                shutil.move(src, dst)
                print(f"    movido: {f}")
            else:
                print(f"    ya existe en destino: {f}")
        # Eliminar carpeta original si quedó vacía
        if not os.listdir(ruta_orig):
            os.rmdir(ruta_orig)
            print(f"    carpeta original eliminada")
    else:
        print(f"  RENOMBRAR: {entry!r} -> {nuevo!r}")
        os.rename(ruta_orig, ruta_nueva)
    renombrados += 1

print(f"\nListo. {renombrados} carpeta(s) procesada(s).")
