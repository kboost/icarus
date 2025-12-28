@echo off
REM Script de instalación para Windows
REM Organizador de Descargas Automático

echo 🚀 Instalando Organizador de Descargas para Windows...

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado. Por favor, instale Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip no está instalado. Por favor, instale pip
    pause
    exit /b 1
)

REM Crear directorio de instalación
set INSTALL_DIR=%APPDATA%\DownloadOrganizer
echo 📁 Creando directorio de instalación: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copiar archivos
echo 📋 Copiando archivos...
copy "download_organizer.py" "%INSTALL_DIR%\" >nul
copy "requirements.txt" "%INSTALL_DIR%\" >nul

REM Instalar dependencias de Python
echo 📦 Instalando dependencias de Python...
cd /d "%INSTALL_DIR%"
pip install -r requirements.txt --user

REM Crear acceso directo en el menú de inicio
echo 🔧 Creando acceso directo...
set SCRIPT_DIR=%~dp0
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\DownloadOrganizer.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '\"%INSTALL_DIR%\download_organizer.py\"'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"

REM Configurar inicio automático con el Programador de Tareas
echo ⚙️ Configurando inicio automático...
schtasks /create /tn "DownloadOrganizer" /tr "python \"%INSTALL_DIR%\download_organizer.py\"" /sc onlogon /ru %USERNAME% /f

echo ✅ Instalación completada!
echo.
echo 🎯 Para iniciar el organizador manualmente:
echo    python "%INSTALL_DIR%\download_organizer.py"
echo.
echo 📂 O busque "DownloadOrganizer" en el menú de inicio
echo.
echo 🔄 Para ver el estado del servicio:
echo    schtasks /query /tn "DownloadOrganizer"
echo.
echo 🛑 Para detener el inicio automático:
echo    schtasks /delete /tn "DownloadOrganizer" /f
echo.
echo 📝 Los logs se guardan en: %INSTALL_DIR%\organizer.log
echo.
pause