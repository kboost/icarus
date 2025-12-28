#!/bin/bash

# Script de instalación para Arch Linux
# Organizador de Descargas Automático

set -e

echo "🚀 Instalando Organizador de Descargas para Arch Linux..."

# Verificar si estamos en Arch Linux
if ! command -v pacman &> /dev/null; then
    echo "❌ Este script es para Arch Linux. Use el script de Windows para otros sistemas."
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "📦 Instalando Python..."
    sudo pacman -S python --noconfirm
fi

# Verificar pip
if ! command -v pip &> /dev/null; then
    echo "📦 Instalando pip..."
    sudo pacman -S python-pip --noconfirm
fi

# Crear directorio de instalación
INSTALL_DIR="$HOME/.local/share/download-organizer"
echo "📁 Creando directorio de instalación: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Copiar archivos
echo "📋 Copiando archivos..."
cp download_organizer.py "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"

# Instalar dependencias de Python
echo "📦 Instalando dependencias de Python..."
cd "$INSTALL_DIR"
pip install -r requirements.txt --user

# Crear script de inicio
echo "🔧 Creando script de inicio..."
cat > "$HOME/.local/bin/download-organizer" << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/download-organizer"
python3 download_organizer.py
EOF

chmod +x "$HOME/.local/bin/download-organizer"

# Configurar servicio systemd
echo "⚙️  Configurando servicio systemd..."
mkdir -p "$HOME/.config/systemd/user"
cp download-organizer.service "$HOME/.config/systemd/user/"

# Reemplazar %h y %i en el servicio
sed -i "s|%h|$HOME|g" "$HOME/.config/systemd/user/download-organizer.service"
sed -i "s|%i|$USER|g" "$HOME/.config/systemd/user/download-organizer.service"

# Recargar systemd y habilitar servicio
systemctl --user daemon-reload
systemctl --user enable download-organizer.service

echo "✅ Instalación completada!"
echo ""
echo "🎯 Para iniciar el organizador manualmente:"
echo "   download-organizer"
echo ""
echo "🔄 Para iniciar el servicio ahora:"
echo "   systemctl --user start download-organizer.service"
echo ""
echo "📊 Para ver el estado del servicio:"
echo "   systemctl --user status download-organizer.service"
echo ""
echo "🛑 Para detener el servicio:"
echo "   systemctl --user stop download-organizer.service"
echo ""
echo "📝 Los logs se guardan en: $INSTALL_DIR/organizer.log"