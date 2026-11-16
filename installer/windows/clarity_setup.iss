; ==============================================================================
; Clarity Programming Language — Windows Inno Setup 6 Configuration
; https://clarity.creebrine.com
; ==============================================================================

#define MyAppName "Clarity"
#define MyAppVersion "0.6.0"
#define MyAppPublisher "creebrine"
#define MyAppURL "https://clarity.creebrine.com"
#define MyAppSupportURL "https://clarity.creebrine.com/docs"
#define MyAppUpdatesURL "https://clarity.creebrine.com/install"
#define MyAppExeName "clarity.exe"

[Setup]
; Basic Application Info
AppId={{E14A8972-2D55-46D9-B5B9-F8D265A1A9C4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppSupportURL}
AppUpdatesURL={#MyAppUpdatesURL}

; Destination Directories
; Defaults to Program Files for Admin, or Local AppData for non-admin
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\..\LICENSE

; Output Configuration
OutputDir=..\..\dist\installer
OutputBaseFilename=Clarity-{#MyAppVersion}-Windows-x64-Setup
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Modern Visual Style & Branding
WizardStyle=modern
WizardSizePercent=100
DisableWelcomePage=no
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Uninstaller Configuration
UninstallDisplayName={#MyAppName} {#MyAppVersion}
UninstallDisplayIcon={app}\{#MyAppExeName}
ChangesEnvironment=yes
ChangesAssociations=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "addtopath"; Description: "Add Clarity to environment PATH (recommended)"; GroupDescription: "Environment Integration:"
Name: "associateclr"; Description: "Associate .clr files with Clarity"; GroupDescription: "File Associations:"; Flags: checkedonce

[Files]
; Main standalone runtime bundle
Source: "..\..\dist\clarity\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Runnable examples
Source: "..\..\examples\*"; DestDir: "{app}\examples"; Flags: ignoreversion recursesubdirs
; License and Documentation References
Source: "..\..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
; File Association: .clr -> ClaritySourceFile
Root: HKA; Subkey: "Software\Classes\.clr"; ValueType: string; ValueData: "ClaritySourceFile"; Flags: uninsdeletevalue; Tasks: associateclr
Root: HKA; Subkey: "Software\Classes\.clr\Content Type"; ValueType: string; ValueData: "text/plain"; Flags: uninsdeletevalue; Tasks: associateclr
Root: HKA; Subkey: "Software\Classes\ClaritySourceFile"; ValueType: string; ValueData: "Clarity Source Code"; Flags: uninsdeletekey; Tasks: associateclr
Root: HKA; Subkey: "Software\Classes\ClaritySourceFile\DefaultIcon"; ValueType: string; ValueData: "{app}\{#MyAppExeName},0"; Flags: uninsdeletekey; Tasks: associateclr

; Default action on double-click: Execute in console and pause so user can inspect output
Root: HKA; Subkey: "Software\Classes\ClaritySourceFile\shell\open"; ValueType: string; ValueData: "Run with Clarity"; Flags: uninsdeletekey; Tasks: associateclr
Root: HKA; Subkey: "Software\Classes\ClaritySourceFile\shell\open\command"; ValueType: string; ValueData: """cmd.exe"" /C """"{app}\{#MyAppExeName}"" ""%1"" & pause"""; Flags: uninsdeletekey; Tasks: associateclr

; Context menu actions: Direct Run and Edit in Notepad
Root: HKA; Subkey: "Software\Classes\ClaritySourceFile\shell\run"; ValueType: string; ValueData: "Run (Direct CLI)"; Flags: uninsdeletekey; Tasks: associateclr
Root: HKA; Subkey: "Software\Classes\ClaritySourceFile\shell\run\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Flags: uninsdeletekey; Tasks: associateclr
Root: HKA; Subkey: "Software\Classes\ClaritySourceFile\shell\edit"; ValueType: string; ValueData: "Edit in Notepad"; Flags: uninsdeletekey; Tasks: associateclr
Root: HKA; Subkey: "Software\Classes\ClaritySourceFile\shell\edit\command"; ValueType: string; ValueData: """notepad.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: associateclr

[Run]
; Optional post-install browser trigger
Filename: "{#MyAppSupportURL}"; Description: "View online documentation ({#MyAppSupportURL})"; Flags: shellexec postinstall skipifsilent nowait unchecked

[Code]
// ==============================================================================
// Pascal Script: Safe Environment PATH Modification & Removal
// ==============================================================================

const
    EnvironmentKey = 'Environment';
    SystemEnvironmentKey = 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment';

function IsInPath(Paths: string; Dir: string): Boolean;
var
    NormalizedPaths: string;
    CleanDir: string;
begin
    CleanDir := RemoveBackslashUnlessRoot(Dir);
    NormalizedPaths := ';' + Uppercase(Paths) + ';';
    Result := (Pos(';' + Uppercase(CleanDir) + ';', NormalizedPaths) > 0) or
              (Pos(';' + Uppercase(CleanDir) + '\;', NormalizedPaths) > 0);
end;

procedure AddPathToEnv();
var
    Paths: string;
    AppDir: string;
    RegRoot: Integer;
    RegKey: string;
begin
    AppDir := RemoveBackslashUnlessRoot(ExpandConstant('{app}'));
    if IsAdminInstallMode() then
    begin
        RegRoot := HKEY_LOCAL_MACHINE;
        RegKey := SystemEnvironmentKey;
    end
    else
    begin
        RegRoot := HKEY_CURRENT_USER;
        RegKey := EnvironmentKey;
    end;

    if RegQueryStringValue(RegRoot, RegKey, 'Path', Paths) then
    begin
        if not IsInPath(Paths, AppDir) then
        begin
            if (Length(Paths) > 0) and (Paths[Length(Paths)] <> ';') then
                Paths := Paths + ';';
            Paths := Paths + AppDir;
            RegWriteExpandStringValue(RegRoot, RegKey, 'Path', Paths);
        end;
    end
    else
    begin
        RegWriteExpandStringValue(RegRoot, RegKey, 'Path', AppDir);
    end;
end;

procedure RemovePathFromEnv();
var
    Paths, CleanPaths: string;
    AppDir: string;
    P, L: Integer;
    RegRoot: Integer;
    RegKey: string;
begin
    AppDir := RemoveBackslashUnlessRoot(ExpandConstant('{app}'));
    if IsAdminInstallMode() then
    begin
        RegRoot := HKEY_LOCAL_MACHINE;
        RegKey := SystemEnvironmentKey;
    end
    else
    begin
        RegRoot := HKEY_CURRENT_USER;
        RegKey := EnvironmentKey;
    end;

    if RegQueryStringValue(RegRoot, RegKey, 'Path', Paths) then
    begin
        CleanPaths := ';' + Paths + ';';
        P := Pos(';' + Uppercase(AppDir) + ';', Uppercase(CleanPaths));
        if P = 0 then
            P := Pos(';' + Uppercase(AppDir) + '\;', Uppercase(CleanPaths));

        if P > 0 then
        begin
            L := Length(AppDir) + 1;
            Delete(CleanPaths, P, L);
            if Length(CleanPaths) > 1 then
            begin
                Delete(CleanPaths, 1, 1);
                Delete(CleanPaths, Length(CleanPaths), 1);
            end
            else
                CleanPaths := '';
            RegWriteExpandStringValue(RegRoot, RegKey, 'Path', CleanPaths);
        end;
    end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
    if CurStep = ssPostInstall then
    begin
        if WizardIsTaskSelected('addtopath') then
        begin
            AddPathToEnv();
        end;
    end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
    if CurUninstallStep = usPostUninstall then
    begin
        RemovePathFromEnv();
    end;
end;
