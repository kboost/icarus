#!/bin/bash

# Instalador del Proyecto Icarus
# Organizador de Descargas Automático con Seguridad

echo "🚀 Proyecto Icarus - Organizador de Descargas Seguro"
echo "====================================================="

# Verificar si estamos en Arch Linux
if command -v pacman &> /dev/null; then
    echo "📦 Detectado Arch Linux"
    ./install_arch.sh
elif [[ "$OS" == "Windows_NT" ]]; then
    echo "📦 Detectado Windows"
    ./install_windows.bat
else
    echo "❌ Sistema no detectado. Ejecuta manualmente:"
    echo "   Arch Linux: ./install_arch.sh"
    echo "   Windows: install_windows.bat"
fi