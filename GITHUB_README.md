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

## 🧪 Demo Rápida

```bash
python3 demo_organizer.py
```

## 📦 Instalación

### Arch Linux
```bash
./install_arch.sh
```

### Windows
```cmd
install_windows.bat
```

## 🛡️ Archivos Sensibles Protegidos

- 🔒 `Contraseñas.csv` - Detectado y protegido
- 🔒 `private_key.pem` - Certificado criptográfico
- 🔒 `system_config.tmp` - Configuración del sistema
- 🔒 `login_credentials.docx` - Credenciales de acceso

## 📊 Organización Automática

- **Imágenes**: `.jpg`, `.png`, `.gif`, `.svg`, `.webp`
- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`
- **Video**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.webm`
- **Documentos**: `.pdf`, `.doc`, `.docx`, `.txt`, `.xls`
- **Comprimidos**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
- **Ejecutables**: `.exe`, `.msi`, `.deb`, `.rpm`, `.dmg`
- **Código**: `.py`, `.js`, `.html`, `.css`, `.cpp`, `.java`

---

**🔒 Icarus: Tu downloads organizados y seguros**