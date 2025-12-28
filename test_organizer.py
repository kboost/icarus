#!/usr/bin/env python3
"""
Organizador de Descargas - Versión de Pruebas Simplificada
Monitorea y organiza archivos sin dependencias externas.
"""

import os
import sys
import time
import shutil
import json
import logging
from pathlib import Path
from datetime import datetime
import platform
import threading

class SimpleDownloadOrganizer:
    def __init__(self):
        self.config_file = "organizer_config.json"
        self.stats_file = "organizer_stats.json"
        self.load_config()
        self.load_stats()
        self.setup_logging()
        
        # Determinar carpeta de descargas
        self.downloads_dir = Path.home() / "Downloads"
        
        # Mapeo de extensiones a carpetas
        self.extension_mapping = {
            '.jpg': 'Imágenes', '.jpeg': 'Imágenes', '.png': 'Imágenes', 
            '.gif': 'Imágenes', '.bmp': 'Imágenes', '.svg': 'Imágenes',
            '.webp': 'Imágenes', '.ico': 'Imágenes',
            '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio', 
            '.aac': 'Audio', '.ogg': 'Audio', '.m4a': 'Audio',
            '.wma': 'Audio',
            '.mp4': 'Video', '.avi': 'Video', '.mkv': 'Video', 
            '.mov': 'Video', '.wmv': 'Video', '.flv': 'Video',
            '.webm': 'Video', '.m4v': 'Video',
            '.pdf': 'Documentos', '.doc': 'Documentos', '.docx': 'Documentos',
            '.txt': 'Documentos', '.rtf': 'Documentos', '.odt': 'Documentos',
            '.xls': 'Documentos', '.xlsx': 'Documentos', '.ppt': 'Documentos',
            '.pptx': 'Documentos', '.ods': 'Documentos', '.odp': 'Documentos',
            '.zip': 'Comprimidos', '.rar': 'Comprimidos', '.7z': 'Comprimidos',
            '.tar': 'Comprimidos', '.gz': 'Comprimidos', '.bz2': 'Comprimidos',
            '.exe': 'Ejecutables', '.msi': 'Ejecutables', '.deb': 'Ejecutables',
            '.rpm': 'Ejecutables', '.dmg': 'Ejecutables', '.pkg': 'Ejecutables',
            '.py': 'Código', '.js': 'Código', '.html': 'Código', '.css': 'Código',
            '.cpp': 'Código', '.c': 'Código', '.java': 'Código', '.php': 'Código',
            '.rb': 'Código', '.go': 'Código', '.rs': 'Código',
        }
        
        self.organized_count = 0
        self.start_time = datetime.now()
        self.running = True
        
    def load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {
                "auto_start": True,
                "show_notifications": True,
                "log_level": "INFO"
            }
    
    def load_stats(self):
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                self.stats = json.load(f)
        except:
            self.stats = {
                "total_organized": 0,
                "by_category": {},
                "by_date": {},
                "start_date": datetime.now().isoformat()
            }
    
    def save_stats(self):
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
    
    def setup_logging(self):
        log_level = getattr(logging, self.config.get("log_level", "INFO"))
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('organizer.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_category(self, file_path):
        ext = file_path.suffix.lower()
        return self.extension_mapping.get(ext, 'Otros')
    
    def organize_file(self, file_path):
        try:
            if not file_path.exists():
                return False
            
            category = self.get_category(file_path)
            category_dir = self.downloads_dir / category
            
            # Crear carpeta si no existe
            category_dir.mkdir(exist_ok=True)
            
            # Generar nombre único si ya existe
            dest_path = category_dir / file_path.name
            counter = 1
            while dest_path.exists():
                stem = file_path.stem
                suffix = file_path.suffix
                dest_path = category_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Mover archivo
            shutil.move(str(file_path), str(dest_path))
            
            # Actualizar estadísticas
            self.organized_count += 1
            self.stats["total_organized"] += 1
            self.stats["by_category"][category] = self.stats["by_category"].get(category, 0) + 1
            
            today = datetime.now().strftime("%Y-%m-%d")
            self.stats["by_date"][today] = self.stats["by_date"].get(today, 0) + 1
            
            self.save_stats()
            
            self.logger.info(f"✅ Archivo organizado: {file_path.name} -> {category}/{dest_path.name}")
            print(f"🎯 [PRUEBA] Archivo organizado: {file_path.name} → {category}/")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error organizando archivo {file_path}: {e}")
            print(f"❌ [PRUEBA] Error: {e}")
            return False
    
    def organize_existing_files(self):
        if not self.downloads_dir.exists():
            self.logger.warning(f"La carpeta de descargas no existe: {self.downloads_dir}")
            print(f"⚠️ [PRUEBA] Carpeta no existe: {self.downloads_dir}")
            return
        
        print(f"🔍 [PRUEBA] Buscando archivos en: {self.downloads_dir}")
        organized = 0
        
        for file_path in self.downloads_dir.iterdir():
            if file_path.is_file():
                print(f"📁 [PRUEBA] Encontrado: {file_path.name}")
                if self.organize_file(file_path):
                    organized += 1
        
        print(f"✅ [PRUEBA] Se organizaron {organized} archivos existentes")
        self.logger.info(f"Se organizaron {organized} archivos existentes")
    
    def monitor_downloads(self):
        print(f"👀 [PRUEBA] Iniciando monitoreo de: {self.downloads_dir}")
        print("🔄 [PRUEBA] Monitoreando nuevos archivos (presiona Ctrl+C para detener)")
        
        # Lista de archivos ya conocidos
        known_files = set()
        if self.downloads_dir.exists():
            known_files = {f.name for f in self.downloads_dir.iterdir() if f.is_file()}
        
        try:
            while self.running:
                if self.downloads_dir.exists():
                    current_files = {f.name for f in self.downloads_dir.iterdir() if f.is_file()}
                    new_files = current_files - known_files
                    
                    for filename in new_files:
                        file_path = self.downloads_dir / filename
                        print(f"🆕 [PRUEBA] Nuevo archivo detectado: {filename}")
                        
                        # Esperar un momento para asegurar que la descarga se completó
                        time.sleep(2)
                        
                        if file_path.exists():
                            self.organize_file(file_path)
                            known_files.add(filename)
                
                time.sleep(3)  # Revisar cada 3 segundos
                
        except KeyboardInterrupt:
            print("\n🛑 [PRUEBA] Monitoreo detenido por el usuario")
            self.running = False
    
    def show_stats(self):
        print(f"\n📊 [PRUEBA] Estadísticas actuales:")
        print(f"   Total organizados: {self.stats['total_organized']}")
        print(f"   Tiempo en ejecución: {datetime.now() - self.start_time}")
        
        if self.stats['by_category']:
            print(f"   Por categoría:")
            for category, count in sorted(self.stats['by_category'].items()):
                print(f"     {category}: {count} archivos")
    
    def create_test_files(self):
        """Crear archivos de prueba para demostrar el funcionamiento"""
        print("🧪 [PRUEBA] Creando archivos de prueba...")
        
        test_files = [
            ("test_image.jpg", "contenido de imagen de prueba"),
            ("test_document.pdf", "contenido de pdf de prueba"),
            ("test_audio.mp3", "contenido de audio de prueba"),
            ("test_video.mp4", "contenido de video de prueba"),
            ("test_code.py", "print('hola mundo')"),
            ("test_comprimido.zip", "contenido de zip de prueba"),
        ]
        
        for filename, content in test_files:
            test_path = self.downloads_dir / filename
            try:
                with open(test_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ [PRUEBA] Creado: {filename}")
            except Exception as e:
                print(f"❌ [PRUEBA] Error creando {filename}: {e}")


def main():
    print("🚀 [PRUEBA] Iniciando Organizador de Descargas - Modo Pruebas")
    print("=" * 60)
    
    organizer = SimpleDownloadOrganizer()
    
    print(f"📁 [PRUEBA] Carpeta de descargas: {organizer.downloads_dir}")
    print(f"⚙️ [PRUEBA] Configuración cargada desde: {organizer.config_file}")
    
    # Crear carpeta de descargas si no existe
    organizer.downloads_dir.mkdir(exist_ok=True)
    
    # Menú de pruebas
    while True:
        print("\n" + "=" * 40)
        print("🧪 MENÚ DE PRUEBAS")
        print("=" * 40)
        print("1. Crear archivos de prueba")
        print("2. Organizar archivos existentes")
        print("3. Iniciar monitoreo en tiempo real")
        print("4. Mostrar estadísticas")
        print("5. Ver logs")
        print("6. Salir")
        print("=" * 40)
        
        try:
            opcion = input("Selecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                organizer.create_test_files()
                
            elif opcion == "2":
                organizer.organize_existing_files()
                
            elif opcion == "3":
                organizer.monitor_downloads()
                
            elif opcion == "4":
                organizer.show_stats()
                
            elif opcion == "5":
                print("\n📝 [PRUEBA] Últimos logs:")
                try:
                    with open('organizer.log', 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in lines[-10:]:  # Últimas 10 líneas
                            print(f"   {line.strip()}")
                except FileNotFoundError:
                    print("   No hay logs aún")
                    
            elif opcion == "6":
                print("👋 [PRUEBA] Saliendo del programa...")
                break
                
            else:
                print("❌ [PRUEBA] Opción no válida. Intenta de nuevo.")
                
        except KeyboardInterrupt:
            print("\n👋 [PRUEBA] Saliendo del programa...")
            break
        except Exception as e:
            print(f"❌ [PRUEBA] Error: {e}")
    
    print("✅ [PRUEBA] Programa finalizado. ¡Gracias por probar!")


if __name__ == "__main__":
    main()