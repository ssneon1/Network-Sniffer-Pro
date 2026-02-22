; ─────────────────────────────────────────────────────────────────
;  Network Sniffer Pro - Inno Setup Installer Script
;  Build with: Inno Setup Compiler (https://jrsoftware.org/isinfo.php)
; ─────────────────────────────────────────────────────────────────

#define AppName      "Network Sniffer Pro"
#define AppVersion   "1.0.0"
#define AppPublisher "ssneon"
#define AppExeName   "main.exe"
#define AppURL       "https://github.com/ssneon1/task1cyber1"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=installer_output
OutputBaseFilename=NetworkSnifferPro_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
; Minimum Windows 10
MinVersion=10.0.17763

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
; Main executable
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Include templates if they exist alongside the EXE
; Source: "dist\templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu shortcut
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional, based on task choice)
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
; Offer to launch the app after install
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Messages]
; Custom welcome message
WelcomeLabel2=This will install [name/ver] on your computer.%n%nIMPORTANT: You must install Npcap (https://npcap.com) before running this application, otherwise packet capture will not work.%n%nClick Next to continue.

[Code]
// Optional: Check for Npcap on install
function NpcapInstalled: Boolean;
var
  RegKey: String;
begin
  RegKey := 'SOFTWARE\Npcap';
  Result := RegKeyExists(HKLM, RegKey) or RegKeyExists(HKLM, 'SOFTWARE\WOW6432Node\Npcap');
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpWelcome then
  begin
    if not NpcapInstalled then
    begin
      MsgBox(
        '⚠️  Npcap Not Detected!' + #13#10 + #13#10 +
        'Network Sniffer Pro requires Npcap to capture network packets.' + #13#10 +
        'Please download and install Npcap from:' + #13#10 +
        'https://npcap.com' + #13#10 + #13#10 +
        'You can continue installation now and install Npcap later.',
        mbInformation, MB_OK);
    end;
  end;
end;
