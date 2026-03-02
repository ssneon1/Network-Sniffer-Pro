@echo off
setlocal

:: ─────────────────────────────────────────────
::  Network Sniffer Pro - Installer Script
::  Run as Administrator
:: ─────────────────────────────────────────────

set "INSTALL_DIR=%ProgramFiles%\Network Sniffer Pro"
set "SOURCE_EXE=%~dp0main.exe"
set "NPCAP_INSTALLER=%~dp0npcap-installer.exe"

echo =========================================
echo   Network Sniffer Pro - Installer
echo =========================================
echo.

:: Check if running as admin
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [!] Please right-click setup.bat and choose "Run as Administrator"
    pause
    exit /b 1
)

:: Check main.exe exists
if not exist "%SOURCE_EXE%" (
    echo [ERROR] main.exe not found in this folder!
    pause
    exit /b 1
)

:: ─── Step 1: Npcap Check ──────────────────────
echo [1/4] Checking for Npcap...
reg query "HKLM\SOFTWARE\Npcap" >nul 2>&1
if %errorLevel% EQU 0 (
    echo       Npcap already installed. Skipping.
    goto INSTALL_APP
)
reg query "HKLM\SOFTWARE\WOW6432Node\Npcap" >nul 2>&1
if %errorLevel% EQU 0 (
    echo       Npcap already installed. Skipping.
    goto INSTALL_APP
)

:: Npcap not found — install it
echo       Npcap not found. Installing...
if not exist "%NPCAP_INSTALLER%" (
    echo [ERROR] npcap-installer.exe not found in this folder!
    echo         Please add the Npcap installer from https://npcap.com
    pause
    exit /b 1
)

:: Run Npcap silently
"%NPCAP_INSTALLER%" /S
if %errorLevel% NEQ 0 (
    echo [WARNING] Npcap installer may have encountered an issue.
    echo           You can install it manually from https://npcap.com
)
echo       Npcap installed successfully.

:INSTALL_APP
:: ─── Step 2: Create install directory ─────────
echo [2/4] Creating installation folder...
mkdir "%INSTALL_DIR%" >nul 2>&1

:: ─── Step 3: Copy the application ─────────────
echo [3/4] Copying application files...
copy /Y "%SOURCE_EXE%" "%INSTALL_DIR%\main.exe" >nul
if %errorLevel% NEQ 0 (
    echo [ERROR] Could not copy files. Run as Administrator.
    pause
    exit /b 1
)

:: ─── Step 4: Desktop Shortcut ─────────────────
echo [4/4] Creating desktop shortcut...
powershell -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $s = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Network Sniffer Pro.lnk'); ^
   $s.TargetPath = '%INSTALL_DIR%\main.exe'; ^
   $s.WorkingDirectory = '%INSTALL_DIR%'; ^
   $s.Description = 'Network Sniffer Pro'; ^
   $s.Save()"

echo.
echo =========================================
echo   Installation Complete!
echo =========================================
echo.
echo  App installed to: %INSTALL_DIR%
echo  Desktop shortcut created.
echo  Launch it from your Desktop!
echo.
pause
