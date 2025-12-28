# Organizador de Descargas Automático

Herramienta para organizar automáticamente los archivos descargados según su tipo, compatible con Arch Linux y Windows.

## 🚀 Características

- **Monitoreo en tiempo real**: Detecta nuevas descargas y las organiza automáticamente
- **Panel de monitoreo**: Interfaz gráfica con estadísticas en vivo
- **Multiplataforma**: Funciona en Arch Linux y Windows
- **Auto-inicio**: Se inicia automáticamente con el sistema
- **Notificaciones**: Alertas cuando se organizan archivos
- **Configurable**: Personalizable mediante archivo JSON

## 📦 Instalación

### Arch Linux

1. Ejecuta el script de instalación:
```bash
./install_arch.sh
```

El script instalará automáticamente:
- Dependencias de Python
- Creará los directorios necesarios
- Configurará el servicio systemd para auto-inicio

### Windows

1. Ejecuta el script de instalación como administrador:
```cmd
install_windows.bat
```

El script instalará automáticamente:
- Dependencias de Python con pip
- Creará acceso directo en el menú de inicio
- Configurará tarea programada para auto-inicio

## 🎯 Uso

### Inicio Manual

**Arch Linux:**
```bash
download-organizer
```

**Windows:**
```cmd
python "%APPDATA%\DownloadOrganizer\download_organizer.py"
```

O busca "DownloadOrganizer" en el menú de inicio.

### Control del Servicio

**Arch Linux (systemd):**
```bash
# Iniciar servicio
systemctl --user start download-organizer.service

# Ver estado
systemctl --user status download-organizer.service

# Detener servicio
systemctl --user stop download-organizer.service

# Ver logs
journalctl --user -u download-organizer.service -f
```

**Windows (Task Scheduler):**
```cmd
# Ver estado
schtasks /query /tn "DownloadOrganizer"

# Detener auto-inicio
schtasks /delete /tn "DownloadOrganizer" /f
```

## 📁 Organización de Archivos

El organizador crea las siguientes carpetas en tu directorio de Descargas:

- **Imágenes**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.ico`
- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`, `.wma`
- **Video**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`
- **Documentos**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`
- **Comprimidos**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`
- **Ejecutables**: `.exe`, `.msi`, `.deb`, `.rpm`, `.dmg`, `.pkg`
- **Código**: `.py`, `.js`, `.html`, `.css`, `.cpp`, `.c`, `.java`, `.php`, `.rb`, `.go`, `.rs`
- **Otros**: Extensiones no reconocidas

## ⚙️ Configuración

Puedes personalizar el comportamiento editando el archivo `organizer_config.json`:

```json
{
  "auto_start": true,
  "minimize_to_tray": true,
  "show_notifications": true,
  "log_level": "INFO",
  "extension_mapping": {
    ".jpg": "Imágenes",
    ".custom": "MiCarpeta"
  }
}
```

### Opciones de Configuración

- `auto_start`: Iniciar automáticamente con el sistema
- `minimize_to_tray`: Minimizar a la bandeja del sistema
- `show_notifications`: Mostrar notificaciones al organizar archivos
- `log_level`: Nivel de logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `extension_mapping`: Mapeo personalizado de extensiones a carpetas

## 📊 Panel de Monitoreo

La interfaz gráfica muestra:

- **Información General**: Ruta de descargas, total organizados, tiempo de ejecución
- **Estadísticas por Carpeta**: Número de archivos y tamaño por categoría
- **Control**: Botones para actualizar, minimizar y detener

## 📝 Logs

Los logs se guardan en:

- **Arch Linux**: `~/.local/share/download-organizer/organizer.log`
- **Windows**: `%APPDATA%\DownloadOrganizer\organizer.log`

## 🔧 Dependencias

Las dependencias se instalan automáticamente durante la instalación:

- `watchdog`: Monitoreo de archivos en tiempo real
- `psutil`: Estadísticas del sistema
- `pillow`: Soporte de imágenes para bandeja del sistema
- `pystray`: Bandeja del sistema
- `win10toast`: Notificaciones en Windows (opcional)

## 🛠️ Solución de Problemas

### Arch Linux

**El servicio no inicia:**
```bash
# Verificar permisos
ls -la ~/.local/share/download-organizer/

# Ver logs del servicio
journalctl --user -u download-organizer.service -f
```

**Dependencias faltantes:**
```bash
# Instalar manualmente
pip install --user watchdog psutil pillow pystray
```

### Windows

**Error de Python:**
- Asegúrate que Python esté instalado y en el PATH
- Ejecuta como administrador si hay problemas de permisos

**Notificaciones no funcionan:**
- Instala win10toast: `pip install win10toast`

## 🔄 Actualización

Para actualizar a una nueva versión:

1. Detén el servicio
2. Reemplaza los archivos del script
3. Reinicia el servicio

## 📄 Licencia

Este proyecto es de código abierto y gratuito.