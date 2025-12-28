#!/usr/bin/env python3
"""
Organizador de Descargas Automático
Monitorea la carpeta de descargas y organiza archivos según su tipo.
Compatible con Arch Linux y Windows.
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
import tkinter as tk
from tkinter import ttk, messagebox

# Intentar importar dependencias opcionales
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("⚠️  Watchdog no instalado. El monitoreo en tiempo real no estará disponible.")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️  Psutil no instalado. Las estadísticas del sistema no estarán disponibles.")

class DownloadOrganizer:
    def __init__(self):
        self.config_file = "organizer_config.json"
        self.stats_file = "organizer_stats.json"
        self.load_config()
        self.load_stats()
        self.setup_logging()
        
        # Determinar carpeta de descargas según el SO
        self.downloads_dir = self.get_downloads_folder()
        
        # Mapeo de extensiones a carpetas
        self.extension_mapping = {
            # Imágenes
            '.jpg': 'Imágenes', '.jpeg': 'Imágenes', '.png': 'Imágenes', 
            '.gif': 'Imágenes', '.bmp': 'Imágenes', '.svg': 'Imágenes',
            '.webp': 'Imágenes', '.ico': 'Imágenes',
            
            # Audio
            '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio', 
            '.aac': 'Audio', '.ogg': 'Audio', '.m4a': 'Audio',
            '.wma': 'Audio',
            
            # Video
            '.mp4': 'Video', '.avi': 'Video', '.mkv': 'Video', 
            '.mov': 'Video', '.wmv': 'Video', '.flv': 'Video',
            '.webm': 'Video', '.m4v': 'Video',
            
            # Documentos
            '.pdf': 'Documentos', '.doc': 'Documentos', '.docx': 'Documentos',
            '.txt': 'Documentos', '.rtf': 'Documentos', '.odt': 'Documentos',
            '.xls': 'Documentos', '.xlsx': 'Documentos', '.ppt': 'Documentos',
            '.pptx': 'Documentos', '.ods': 'Documentos', '.odp': 'Documentos',
            
            # Comprimidos
            '.zip': 'Comprimidos', '.rar': 'Comprimidos', '.7z': 'Comprimidos',
            '.tar': 'Comprimidos', '.gz': 'Comprimidos', '.bz2': 'Comprimidos',
            
            # Ejecutables
            '.exe': 'Ejecutables', '.msi': 'Ejecutables', '.deb': 'Ejecutables',
            '.rpm': 'Ejecutables', '.dmg': 'Ejecutables', '.pkg': 'Ejecutables',
            
            # Código
            '.py': 'Código', '.js': 'Código', '.html': 'Código', '.css': 'Código',
            '.cpp': 'Código', '.c': 'Código', '.java': 'Código', '.php': 'Código',
            '.rb': 'Código', '.go': 'Código', '.rs': 'Código',
        }
        
        self.organized_count = 0
        self.start_time = datetime.now()
        
    def get_downloads_folder(self):
        """Obtener la carpeta de descargas según el sistema operativo"""
        if platform.system() == "Windows":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
                downloads = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
                winreg.CloseKey(key)
                return Path(downloads)
            except:
                return Path.home() / "Downloads"
        else:
            return Path.home() / "Downloads"
    
    def load_config(self):
        """Cargar configuración desde archivo"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {
                "auto_start": True,
                "minimize_to_tray": True,
                "show_notifications": True,
                "log_level": "INFO"
            }
    
    def save_config(self):
        """Guardar configuración en archivo"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def load_stats(self):
        """Cargar estadísticas desde archivo"""
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
        """Guardar estadísticas en archivo"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
    
    def setup_logging(self):
        """Configurar sistema de logging"""
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
        """Determinar la categoría de un archivo según su extensión"""
        ext = file_path.suffix.lower()
        return self.extension_mapping.get(ext, 'Otros')
    
    def organize_file(self, file_path):
        """Organizar un archivo en su carpeta correspondiente"""
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
            
            self.logger.info(f"Archivo organizado: {file_path.name} -> {category}/{dest_path.name}")
            
            if self.config.get("show_notifications", True):
                self.show_notification(f"Archivo organizado: {file_path.name}", category)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error organizando archivo {file_path}: {e}")
            return False
    
    def show_notification(self, title, message):
        """Mostrar notificación del sistema"""
        try:
            if platform.system() == "Windows":
                try:
                    import win10toast
                    toaster = win10toast.ToastNotifier()
                    toaster.show_toast(title, message, duration=3)
                except ImportError:
                    pass
            else:
                # Para Linux, usar notify-send si está disponible
                os.system(f"notify-send '{title}' '{message}' 2>/dev/null")
        except:
            pass  # Silenciosamente fallar si no hay notificaciones
    
    def get_folder_size(self, folder_path):
        """Obtener tamaño total de una carpeta"""
        try:
            total_size = 0
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            return total_size
        except:
            return 0
    
    def get_folder_stats(self):
        """Obtener estadísticas de todas las carpetas"""
        stats = {}
        for category in set(self.extension_mapping.values()) | {'Otros'}:
            category_dir = self.downloads_dir / category
            if category_dir.exists():
                file_count = len(list(category_dir.rglob('*')))
                size_bytes = self.get_folder_size(category_dir)
                stats[category] = {
                    'file_count': file_count,
                    'size_bytes': size_bytes,
                    'size_mb': round(size_bytes / (1024 * 1024), 2)
                }
        return stats
    
    def organize_existing_files(self):
        """Organizar archivos existentes en la carpeta de descargas"""
        if not self.downloads_dir.exists():
            self.logger.warning(f"La carpeta de descargas no existe: {self.downloads_dir}")
            return
        
        organized = 0
        for file_path in self.downloads_dir.iterdir():
            if file_path.is_file():
                if self.organize_file(file_path):
                    organized += 1
        
        self.logger.info(f"Se organizaron {organized} archivos existentes")


class DownloadEventHandler(FileSystemEventHandler):
    def __init__(self, organizer):
        self.organizer = organizer
        self.cooldown = {}
        self.cooldown_time = 2  # Segundos de espera para evitar procesamiento múltiple
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Evitar procesamiento múltiple del mismo archivo
        file_key = str(file_path)
        current_time = time.time()
        
        if file_key in self.cooldown:
            if current_time - self.cooldown[file_key] < self.cooldown_time:
                return
        
        self.cooldown[file_key] = current_time
        
        # Pequeña espera para asegurar que la descarga se completó
        time.sleep(1)
        
        if file_path.exists():
            self.organizer.organize_file(file_path)


class MonitorGUI:
    def __init__(self, organizer):
        self.organizer = organizer
        self.root = tk.Tk()
        self.root.title("Organizador de Descargas - Monitor")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.setup_ui()
        self.update_stats()
        
    def setup_ui(self):
        """Configurar la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="📁 Organizador de Descargas", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Información general
        info_frame = ttk.LabelFrame(main_frame, text="Información General", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.downloads_path_label = ttk.Label(info_frame, 
                                              text=f"Carpeta de descargas: {self.organizer.downloads_dir}")
        self.downloads_path_label.grid(row=0, column=0, sticky="w")
        
        self.total_organized_label = ttk.Label(info_frame, text="Total organizados: 0")
        self.total_organized_label.grid(row=1, column=0, sticky="w")
        
        self.uptime_label = ttk.Label(info_frame, text="Tiempo en ejecución: 00:00:00")
        self.uptime_label.grid(row=2, column=0, sticky="w")
        
        # Estadísticas por carpeta
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas por Carpeta", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Treeview para estadísticas
        columns = ('Archivos', 'Tamaño')
        self.stats_tree = ttk.Treeview(stats_frame, columns=columns, height=10)
        self.stats_tree.heading('#0', text='Carpeta')
        self.stats_tree.heading('Archivos', text='Archivos')
        self.stats_tree.heading('Tamaño', text='Tamaño')
        
        self.stats_tree.column('#0', width=150)
        self.stats_tree.column('Archivos', width=100)
        self.stats_tree.column('Tamaño', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        self.stats_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        self.refresh_button = ttk.Button(button_frame, text="🔄 Actualizar", 
                                        command=self.update_stats)
        self.refresh_button.grid(row=0, column=0, padx=(0, 10))
        
        self.minimize_button = ttk.Button(button_frame, text="📉 Minimizar", 
                                         command=self.minimize_to_tray)
        self.minimize_button.grid(row=0, column=1, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="⏹ Detener", 
                                     command=self.stop_organizer)
        self.stop_button.grid(row=0, column=2)
        
    def update_stats(self):
        """Actualizar estadísticas en la GUI"""
        # Limpiar treeview
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        # Obtener estadísticas
        folder_stats = self.organizer.get_folder_stats()
        
        # Agregar datos al treeview
        for category, stats in sorted(folder_stats.items()):
            size_text = f"{stats['size_mb']} MB"
            if stats['size_mb'] > 1024:
                size_text = f"{stats['size_mb']/1024:.2f} GB"
            
            self.stats_tree.insert('', 'end', text=category, 
                                   values=(stats['file_count'], size_text))
        
        # Actualizar etiquetas
        self.total_organized_label.config(
            text=f"Total organizados: {self.organizer.stats['total_organized']}")
        
        # Actualizar tiempo de ejecución
        uptime = datetime.now() - self.organizer.start_time
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.uptime_label.config(
            text=f"Tiempo en ejecución: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Programar próxima actualización
        self.root.after(5000, self.update_stats)  # Actualizar cada 5 segundos
    
    def minimize_to_tray(self):
        """Minimizar a la bandeja del sistema"""
        self.root.withdraw()
        
        if platform.system() == "Windows":
            try:
                import pystray
                from PIL import Image
                
                def show_window(icon, item):
                    self.root.deiconify()
                
                # Crear ícono simple
                image = Image.new('RGB', (64, 64), color='blue')
                icon = pystray.Icon("organizer", image, "Organizador de Descargas", 
                                   menu=pystray.Menu(pystray.MenuItem("Mostrar", show_window)))
                icon.run()
            except ImportError:
                self.root.deiconify()
        else:
            # Para Linux, simplemente ocultar y mostrar con atajo
            self.root.bind('<Control><h>', lambda e: self.root.deiconify())
    
    def stop_organizer(self):
        """Detener el organizador"""
        if messagebox.askyesno("Confirmar", "¿Desea detener el organizador de descargas?"):
            self.root.quit()
    
    def run(self):
        """Ejecutar la GUI"""
        self.root.mainloop()


def main():
    """Función principal"""
    print("🚀 Iniciando Organizador de Descargas...")
    
    # Verificar dependencias
    if not WATCHDOG_AVAILABLE:
        print("⚠️  Para monitoreo en tiempo real, instale: pip install watchdog")
    
    # Crear organizador
    organizer = DownloadOrganizer()
    
    print(f"📁 Monitoreando: {organizer.downloads_dir}")
    
    # Organizar archivos existentes
    organizer.organize_existing_files()
    
    # Configurar observador de archivos si está disponible
    observer = None
    if WATCHDOG_AVAILABLE:
        event_handler = DownloadEventHandler(organizer)
        observer = Observer()
        observer.schedule(event_handler, str(organizer.downloads_dir), recursive=False)
        observer.start()
        print("👀 Monitoreo en tiempo real activado")
    else:
        print("⚠️  Ejecutando sin monitoreo en tiempo real")
    
    # Iniciar GUI en un hilo separado
    def run_gui():
        gui = MonitorGUI(organizer)
        gui.run()
    
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo organizador...")
        if observer:
            observer.stop()
            observer.join()
        print("✅ Organizador detenido.")


if __name__ == "__main__":
    main()