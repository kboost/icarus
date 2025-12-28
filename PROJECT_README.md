# 📦 Proyecto Icarus - Organizador de Descargas Seguro

Herramienta inteligente para organizar automáticamente los archivos descargados según su tipo, con protección de archivos sensibles y monitoreo en tiempo real.

## 🛡️ Características de Seguridad

- **Protección de archivos sensibles:** Detecta y protege archivos con contraseñas, claves, tokens y configuraciones
- **Análisis inteligente:** Examina el contenido de archivos CSV para detectar información sensible
- **Extensiones seguras:** Solo organiza archivos con extensiones reconocidas y seguras
- **Logs completos:** Registra cada decisión de seguridad tomada

## 🚀 Características Principales

- **Monitoreo en tiempo real:** Detecta nuevas descargas y las organiza automáticamente
- **Panel de monitoreo:** Interfaz gráfica con estadísticas en vivo
- **Multiplataforma:** Funciona en Arch Linux y Windows
- **Auto-inicio:** Se inicia automáticamente con el sistema
- **Notificaciones:** Alertas cuando se organizan archivos
- **Configurable:** Personalizable mediante archivo JSON

## 📁 Estructura del Proyecto

```
icarus/
├── README.md                    # Este archivo
├── install.sh                   # Instalador universal
├── install_arch.sh              # Instalador para Arch Linux
├── install_windows.bat          # Instalador para Windows
├── download_organizer.py        # Script principal con GUI
├── demo_organizer.py            # Demo con seguridad mejorada
├── test_organizer.py            # Versión de pruebas interactiva
├── requirements.txt              # Dependencias Python
├── organizer_config.json        # Configuración predeterminada
├── download-organizer.service   # Servicio systemd para Linux
├── download_organizer.tar.gz    # Archivo comprimido del proyecto
└── logs/                        # Logs de ejecución (se crean al usar)
```

## 🛡️ Archivos Sensibles Protegidos

### Palabras Prohibidas
- password, contraseña, pass, login, credential, auth
- token, key, private, secret, config, system
- setup, install, boot, startup, registry, ssh

### Extensiones Peligrosas
- `.key`, `.pem`, `.p12`, `.crt`, `.ppk` - Certificados y claves
- `.bak`, `.backup`, `.tmp`, `.log` - Archivos de sistema
- Cualquier extensión no reconocida

### Ejemplos de Archivos Protegidos
- `Contraseñas.csv` - Detectado y protegido
- `private_key.pem` - Certificado criptográfico
- `system_config.tmp` - Configuración del sistema
- `login_credentials.docx` - Credenciales de acceso

## 📦 Instalación

### Método Automático
```bash
cd icarus
./install.sh
```

### Método Manual

**Arch Linux:**
```bash
./install_arch.sh
```

**Windows:**
```cmd
install_windows.bat
```

## 🎯 Uso

### Demo Rápida (Recomendado para pruebas)
```bash
python3 demo_organizer.py
```

### Versión Completa con GUI
```bash
python3 download_organizer.py
```

### Versión Interactiva de Pruebas
```bash
python3 test_organizer.py
```

## 📊 Organización de Archivos

El organizador crea automáticamente estas carpetas en tu directorio de Descargas:

- **Imágenes**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.ico`
- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`, `.wma`
- **Video**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`
- **Documentos**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.xls`, `.xlsx`, `.ppt`, `.pptx`
- **Comprimidos**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`
- **Ejecutables**: `.exe`, `.msi`, `.deb`, `.rpm`, `.dmg`, `.pkg`
- **Código**: `.py`, `.js`, `.html`, `.css`, `.cpp`, `.c`, `.java`, `.php`, `.rb`, `.go`, `.rs`

## 🔧 Configuración

Edita `organizer_config.json` para personalizar:

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

## 📝 Logs y Monitoreo

Los logs se guardan automáticamente:
- `organizer.log` - Logs del sistema principal
- `demo_organizer.log` - Logs de las demos
- `organizer_stats.json` - Estadísticas de uso

## 🔄 Descarga del Proyecto Completo

Para descargar el proyecto completo:
```bash
# Copiar carpeta completa
cp -r /home/kris/icarus /ruta/destino/

# O descargar archivo comprimido
scp /home/kris/icarus/download_organizer.tar.gz usuario@servidor:~
```

## 🧪 Pruebas de Seguridad

El proyecto incluye una demostración automática que muestra:
- ✅ Organización correcta de archivos seguros
- 🔒 Protección de archivos sensibles
- 📊 Estadísticas detalladas
- 📝 Logs completos

Ejecuta `python3 demo_organizer.py` para ver la demostración completa.

## 🛠️ Dependencias

Las dependencias se instalan automáticamente durante la instalación:
- `watchdog` - Monitoreo de archivos en tiempo real
- `psutil` - Estadísticas del sistema
- `pillow` - Soporte de imágenes para bandeja del sistema
- `pystray` - Bandeja del sistema
- `win10toast` - Notificaciones en Windows (opcional)

## 📄 Licencia

Este proyecto es de código abierto y gratuito. Orientado a la seguridad y privacidad del usuario.

---

**🔒 Icarus: Tu downloads organizados y seguros**