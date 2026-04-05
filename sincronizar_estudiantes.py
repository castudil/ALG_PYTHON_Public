import os
import shutil
import subprocess
from pathlib import Path

# Configuracion
PRIVATE_REPO = Path(__file__).parent.resolve()
PUBLIC_REPO = PRIVATE_REPO.parent / "ALG_PYTHON_Public"

# Archivos o carpetas a ignorar por completo
IGNORE_DIRS = {".git", ".venv", ".ipynb_checkpoints", "__pycache__", "00_Gestion_Administrativa", "02_Evaluaciones_Vault", "04_Legacy_ppt", "03_Legacy_Java"}
IGNORE_EXTS = {".DS_Store"}

def should_copy(item_path: Path) -> bool:
    """ Determina si un archivo debe ser copiado al repositorio publico. """
    # Ignoramos si es un directorio restringido
    if item_path.is_dir() and item_path.name in IGNORE_DIRS:
        return False
        
    if item_path.is_file():
        # Ignoramos por extension
        if item_path.suffix in IGNORE_EXTS:
            return False
        
        # OMITIR las soluciones siempre
        if "SOL" in item_path.name.upper():
            return False
            
        # Solo copiar archivos que explícitamente sean LAB o TEO
        # O si son archivos base necesarios (como README.md)
        name_upper = item_path.name.upper()
        if "LAB" in name_upper or "TEO" in name_upper or name_upper == "README.MD":
            return True

        # Copiar archivos .py auxiliares (ej: unionfind.py) que el estudiante importa directamente
        if item_path.suffix == ".py":
            return True
            
        # Si no cumple ninguna, no se copia
        return False

    return True # Es un directorio permitido

def sync_repos():
    print(f"Sincronizando de {PRIVATE_REPO} -> {PUBLIC_REPO}")
    
    # Crear repo publico si no existe
    if not PUBLIC_REPO.exists():
        PUBLIC_REPO.mkdir(parents=True)
        print(f"Directorio público creado en {PUBLIC_REPO}")
        subprocess.run(["git", "init"], cwd=PUBLIC_REPO)
        
    # Recorrer repositorio privado
    copied_files_count = 0
    
    for root, dirs, files in os.walk(PRIVATE_REPO):
        current_dir = Path(root)
        
        # Remover directorios ignorados para no bajar por ellos en os.walk
        dirs[:] = [d for d in dirs if current_dir / d not in PRIVATE_REPO.parents and should_copy(current_dir / d)]
        
        # Directorio relativo
        rel_path = current_dir.relative_to(PRIVATE_REPO)
        target_dir = PUBLIC_REPO / rel_path
        
        # Asegurar que existe el directorio de destino
        if not target_dir.exists() and rel_path != Path('.'):
            target_dir.mkdir(parents=True, exist_ok=True)
            
        for file in files:
            file_path = current_dir / file
            if should_copy(file_path):
                target_file_path = target_dir / file
                # Solo copiar si es más nuevo o si hay cambio en tamaño
                if not target_file_path.exists() or \
                   target_file_path.stat().st_mtime < file_path.stat().st_mtime or \
                   target_file_path.stat().st_size != file_path.stat().st_size:
                    
                    try:
                        shutil.copy2(file_path, target_file_path)
                        print(f"Copiado: {rel_path / file}")
                        copied_files_count += 1
                    except Exception as e:
                        print(f"Error copiando {file_path}: {e}")

    print(f"Sincronización terminada. Archivos actualizados/copiados: {copied_files_count}")

    print("\n[!] Para publicar los cambios en GitHub, dirígete a la carpeta ALG_PYTHON_Public y ejecuta:")
    print("    git add .")
    print("    git commit -m \"Actualización de material público\"")
    print("    git push origin main")

if __name__ == "__main__":
    sync_repos()
