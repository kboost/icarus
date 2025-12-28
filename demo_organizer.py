#!/usr/bin/env python3
"""
Organizador de Descargas - Demo Automática
Ejecuta una demostración completa del funcionamiento.
"""

import os
import sys
import time
import shutil
import json
import logging
from pathlib import Path
from datetime import datetime

class DemoOrganizer:
    def __init__(self):
        self.downloads_dir = Path.home() / "Downloads"
        # Archivos sensibles que NUNCA deben organizarse
        self.forbidden_files = {
            'passwords', 'password', 'pass', 'contraseña', 'contrasena',
            'login', 'credential', 'credentials', 'auth', 'authentication',
            'token', 'key', 'private', 'secret', 'config', 'configuration',
            'setup', 'install', 'boot', 'startup', 'system', 'registry',
            'hosts', 'ssh', 'rsa', 'pem', 'crt', 'keychain', 'wallet'
        }
        
        # Extensiones de archivos sensibles
        self.forbidden_extensions = {
            '.p12', '.pfx', '.key', '.pem', '.crt', '.der', '.csr',
            '.ppk', '.bak', '.backup', '.tmp', '.temp', '.log'
        }
        
        # Extensiones que SÍ deben organizarse
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
        
        self.stats = {
            "total_organized": 0,
            "by_category": {},
            "start_date": datetime.now().isoformat()
        }
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('demo_organizer.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def is_sensitive_file(self, file_path):
        """Verificar si un archivo es sensible y no debe organizarse"""
        filename = file_path.name.lower()
        extension = file_path.suffix.lower()
        
        # Verificar extensión prohibida
        if extension in self.forbidden_extensions:
            return True
        
        # Verificar nombre de archivo con palabras prohibidas
        for forbidden in self.forbidden_files:
            if forbidden in filename:
                return True
        
        # Verificar archivos CSV que puedan contener contraseñas
        if extension == '.csv':
            sensitive_keywords = ['password', 'contraseña', 'login', 'credential', 'secret']
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    first_lines = ''.join(f.readlines()[:5])  # Leer primeras 5 líneas
                    for keyword in sensitive_keywords:
                        if keyword in first_lines.lower():
                            return True
            except:
                pass  # Si no puede leer el archivo, asumir que es sensible
        
        return False
    
    def get_category(self, file_path):
        ext = file_path.suffix.lower()
        return self.extension_mapping.get(ext, 'Otros')
    
    def organize_file(self, file_path):
        try:
            if not file_path.exists():
                return False
            
            # Verificar si es un archivo sensible
            if self.is_sensitive_file(file_path):
                self.logger.warning(f"⚠️ Archivo sensible ignorado: {file_path.name}")
                print(f"🔒 [DEMO] Archivo sensible IGNORADO: {file_path.name}")
                return False
            
            # Verificar si es una extensión reconocida
            category = self.get_category(file_path)
            if category == 'Otros':
                self.logger.info(f"ℹ️ Extensión no reconocida: {file_path.name}")
                print(f"📝 [DEMO] Extensión no reconocida: {file_path.name} (IGNORADO)")
                return False
            
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
            self.stats["total_organized"] += 1
            self.stats["by_category"][category] = self.stats["by_category"].get(category, 0) + 1
            
            self.logger.info(f"✅ Archivo organizado: {file_path.name} -> {category}/{dest_path.name}")
            print(f"🎯 [DEMO] Archivo organizado: {file_path.name} → {category}/")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error organizando archivo {file_path}: {e}")
            print(f"❌ [DEMO] Error: {e}")
            return False
    
    def create_demo_files(self):
        """Crear archivos de demostración"""
        print("🧪 [DEMO] Creando archivos de demostración...")
        
        demo_files = [
            ("vacaciones.jpg", "foto de vacaciones"),
            ("documento_importante.pdf", "contenido pdf"),
            ("cancion_favorita.mp3", "audio de prueba"),
            ("pelicula.mkv", "video de prueba"),
            ("script_python.py", "print('hola mundo')"),
            ("backup.zip", "contenido comprimido"),
            ("instalador.exe", "ejecutable de prueba"),
            ("pagina_web.html", "<html><body>Hola</body></html>"),
            ("imagen.png", "contenido de imagen"),
            ("audio.wav", "contenido de audio wav"),
            # Archivos sensibles que deben ser ignorados
            ("Contraseñas de Brave.csv", "email,password\nuser@example.com,mypass123\nadmin@site.com,secret456"),
            ("passwords.txt", "mi_contraseña_secreta"),
            ("login_credentials.docx", "usuario: admin, contraseña: 123456"),
            ("private_key.pem", "-----BEGIN PRIVATE KEY-----"),
            ("system_config.tmp", "configuración del sistema"),
            ("backup_key.p12", "certificado de seguridad"),
            ("ssh_host_key", "clave SSH del servidor"),
        ]
        
        created = 0
        for filename, content in demo_files:
            test_path = self.downloads_dir / filename
            try:
                with open(test_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ [DEMO] Creado: {filename}")
                created += 1
                time.sleep(0.2)  # Pequeña pausa entre creaciones
            except Exception as e:
                print(f"❌ [DEMO] Error creando {filename}: {e}")
        
        print(f"📊 [DEMO] Se crearon {created} archivos de prueba")
        return created
    
    def organize_all_files(self):
        """Organizar todos los archivos en la carpeta de descargas"""
        print(f"🔍 [DEMO] Buscando archivos en: {self.downloads_dir}")
        
        if not self.downloads_dir.exists():
            print(f"⚠️ [DEMO] La carpeta no existe, creándola...")
            self.downloads_dir.mkdir(exist_ok=True)
            return 0
        
        organized = 0
        files_found = []
        
        for file_path in self.downloads_dir.iterdir():
            if file_path.is_file():
                files_found.append(file_path)
                print(f"📁 [DEMO] Encontrado: {file_path.name}")
        
        print(f"📊 [DEMO] Total archivos encontrados: {len(files_found)}")
        
        for file_path in files_found:
            if self.organize_file(file_path):
                organized += 1
            time.sleep(0.3)  # Pausa para ver el proceso
        
        return organized
    
    def show_results(self):
        """Mostrar resultados de la demostración"""
        print("\n" + "="*60)
        print("📊 [DEMO] RESULTADOS DE LA DEMOSTRACIÓN")
        print("="*60)
        
        print(f"📁 Carpeta monitoreada: {self.downloads_dir}")
        print(f"📈 Total archivos organizados: {self.stats['total_organized']}")
        
        if self.stats['by_category']:
            print(f"\n📂 Archivos por categoría:")
            for category, count in sorted(self.stats['by_category'].items()):
                print(f"   📁 {category}: {count} archivos")
                
                # Mostrar contenido de cada carpeta
                category_dir = self.downloads_dir / category
                if category_dir.exists():
                    files = list(category_dir.iterdir())
                    for file in files[:3]:  # Mostrar máximo 3 archivos por categoría
                        size = file.stat().st_size if file.is_file() else 0
                        print(f"      📄 {file.name} ({size} bytes)")
                    if len(files) > 3:
                        print(f"      ... y {len(files) - 3} archivos más")
        
        print(f"\n⏰ Tiempo de ejecución: {datetime.now() - datetime.fromisoformat(self.stats['start_date'])}")
        print(f"📝 Logs guardados en: demo_organizer.log")
        
        # Verificar estructura de carpetas
        print(f"\n📂 Estructura creada:")
        for category in sorted(set(self.extension_mapping.values()) | {'Otros'}):
            category_dir = self.downloads_dir / category
            if category_dir.exists():
                file_count = len(list(category_dir.iterdir()))
                if file_count > 0:
                    print(f"   ✅ {category}/ ({file_count} archivos)")
    
    def simulate_download(self, filename, content):
        """Simular una nueva descarga"""
        print(f"🆕 [DEMO] Simulando descarga: {filename}")
        
        test_path = self.downloads_dir / filename
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        time.sleep(1)  # Simular tiempo de descarga
        
        if self.organize_file(test_path):
            print(f"✅ [DEMO] Descarga organizada automáticamente")
            return True
        return False
    
    def run_demo(self):
        """Ejecutar demostración completa"""
        print("🚀 [DEMO] INICIANDO DEMOSTRACIÓN COMPLETA")
        print("="*60)
        
        # Paso 1: Crear carpeta si no existe
        self.downloads_dir.mkdir(exist_ok=True)
        
        # Paso 2: Crear archivos de prueba
        created = self.create_demo_files()
        
        # Paso 3: Organizar archivos existentes
        print(f"\n🔄 [DEMO] Organizando archivos existentes...")
        organized = self.organize_all_files()
        
        # Paso 4: Simular nuevas descargas
        print(f"\n🔄 [DEMO] Simulando nuevas descargas...")
        time.sleep(2)
        
        new_files = [
            ("nueva_foto.gif", "imagen gif"),
            ("nuevo_documento.docx", "documento word"),
            ("nuevo_audio.flac", "audio flac"),
            # Archivos sensibles que deben ser ignorados
            ("secret_passwords.csv", "user,password\ntest,secret123\nadmin,adminpass"),
            ("auth_tokens.txt", "token_abc123, token_def456"),
        ]
        
        for filename, content in new_files:
            self.simulate_download(filename, content)
            time.sleep(1)
        
        # Paso 5: Mostrar resultados finales
        self.show_results()
        
        print(f"\n✅ [DEMO] ¡Demostración completada con éxito!")
        print(f"💡 [DEMO] Ahora puedes revisar las carpetas organizadas en: {self.downloads_dir}")


def main():
    print("🎬 [DEMO] ORGANIZADOR DE DESCARGAS - DEMOSTRACIÓN AUTOMÁTICA")
    print("Esta demostración mostrará cómo el organizador clasifica archivos automáticamente")
    print()
    
    try:
        demo = DemoOrganizer()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n🛑 [DEMO] Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ [DEMO] Error en la demostración: {e}")
    
    print("\n👋 [DEMO] ¡Gracias por probar el organizador de descargas!")


if __name__ == "__main__":
    main()