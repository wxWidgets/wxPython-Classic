;------------------------------------------------------------------------------
; Editra Windows Installer Build Script
; Author: Cody Precord
; Language: NSIS
; Licence: wxWindows License
;------------------------------------------------------------------------------


;------------------------------ Start MUI Setup -------------------------------

; Global Variables
!define PRODUCT_NAME "Editra"
!define PRODUCT_VERSION "0.7.20"
!define PRODUCT_PUBLISHER "Cody Precord"
!define PRODUCT_WEB_SITE "http://editra.org"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\${PRODUCT_NAME}.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "pixmaps\editra.ico"
!define MUI_UNICON "pixmaps\editra.ico"
!define MUI_FILEICON "pixmaps\editra_doc.png"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page (Read the Licence)
!insertmacro MUI_PAGE_LICENSE "COPYING"
; Components Page (Select what parts to install)
!insertmacro MUI_PAGE_COMPONENTS
; Directory page (Set Where to Install)
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page (Do the installation)
!insertmacro MUI_PAGE_INSTFILES
; Finish page (Post installation tasks)
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Run Editra"
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchEditra"
!insertmacro MUI_PAGE_FINISH

; Un-Installer pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_COMPONENTS
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language files
!insertmacro MUI_LANGUAGE "English"

; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

;------------------------------- End MUI Setup --------------------------------

 
;------------------------------ Start Installer -------------------------------

;---- Constants
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "editra.win32.${PRODUCT_VERSION}.exe"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

RequestExecutionLevel admin 

;---- !defines for use with SHChangeNotify
!ifdef SHCNE_ASSOCCHANGED
!undef SHCNE_ASSOCCHANGED
!endif
!define SHCNE_ASSOCCHANGED 0x08000000

!ifdef SHCNF_FLUSH
!undef SHCNF_FLUSH
!endif
!define SHCNF_FLUSH        0x1000

; Prepare for installation
Function .onInit
  ; prevent running multiple instances of the installer
  System::Call 'kernel32::CreateMutexA(i 0, i 0, t "editra_installer") i .r1 ?e'
  Pop $R0
  StrCmp $R0 0 +3
    MessageBox MB_OK|MB_ICONEXCLAMATION "The installer is already running."
    Abort

  ; Check for existing installation warn before installing new one
  ReadRegStr $R0 ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString"
  StrCmp $R0 "" done

  MessageBox MB_YESNO|MB_ICONEXCLAMATION \
  "An existing installation of Editra has been found. $\nDo you want to remove the previous version before installing $(^Name) ?" \
  IDNO done

  ; Run the uninstaller
  ClearErrors
  ExecWait '$R0 _?=$INSTDIR' ; Do not copy the uninstaller to a temp file

  done:
FunctionEnd

; Extract the files from the installer to the install location
Section "Editra Core" SEC01
  SectionIn RO 1 2

  ; Check that Editra is not running before starting to copy the files
  FindProcDLL::FindProc "${PRODUCT_NAME}.exe"
  StrCmp $R0 0 continueInstall
    MessageBox MB_ICONSTOP|MB_OK "${PRODUCT_NAME} is still running please close all running instances and try to install again"
    Abort
  continueInstall:

  ; Extract the files and make shortcuts
  SetOverwrite try
  SetOutPath "$INSTDIR\"
  File /r ".\*.*"

  ; Add the shortcuts to the start menu and desktop
  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe" "" "$INSTDIR\${MUI_ICON}"
  CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe"  "" "$INSTDIR\${MUI_ICON}"
SectionEnd

; Enabled if Add openwith entry is checked
Section "Context Menus" SEC02
  SectionIn 1
  WriteRegStr HKCR "*\shell\OpenWithEditra" "" "Edit with ${PRODUCT_NAME}"
  WriteRegStr HKCR "*\shell\OpenWithEditra\command" "" '$INSTDIR\${PRODUCT_NAME}.exe "%1"'
;  WriteRegStr HKCR "*\shell\OpenWithEditra\DefaultIcon" "" "${MUI_FILEICON}"

  ; Notify of the shell extension changes
  System::Call 'Shell32::SHChangeNotify(i ${SHCNE_ASSOCCHANGED}, i ${SHCNF_FLUSH}, i 0, i 0)'
SectionEnd

; Add QuickLaunch Icon (That small icon bar next to the start button)
Section "Add Quick Launch Icon" SEC03
  SectionIn 1
  CreateShortCut "$QUICKLAUNCH\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe"
SectionEnd

; Make/Install Shortcut links
Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  SetShellVarContext all
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk" "$INSTDIR\uninst.exe" "" "$INSTDIR\${MUI_UNICON}"
SectionEnd

; Post installation setup
Section -Post
  ;---- Write registry keys for uninstaller
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\${PRODUCT_NAME}.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\${MUI_UNICON}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

; Called if Run Editra is checked on the last page of installer
Function LaunchEditra
  Exec '"$INSTDIR\${PRODUCT_NAME}.exe" "$INSTDIR\CHANGELOG" '
FunctionEnd

; Description Texts for Component page
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} "Required core program files"
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} "Add context menu item 'Edit with ${PRODUCT_NAME}'"
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC03} "Add shortcut to Quick Launch Bar"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;------------------------------- End Installer --------------------------------

;----------------------------- Start Uninstaller ------------------------------

;Function un.onInit
;FunctionEnd

; Cleans up registry, links, and main program files
Section "un.Program Data" UNSEC01
  SectionIn RO 1

  ; Ensure shortcuts are removed from user directory as well
  RmDir /r "$SMPROGRAMS\${PRODUCT_NAME}"
  Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
  Delete "$QUICKLAUNCH\${PRODUCT_NAME}.lnk"
  
  ; Remove all shortcuts from All Users directory
  SetShellVarContext all
  RmDir /r "$SMPROGRAMS\${PRODUCT_NAME}"
  Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
  Delete "$QUICKLAUNCH\${PRODUCT_NAME}.lnk"

  ; Cleanup Registry
  DeleteRegKey HKCR "*\shell\OpenWithEditra"
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"

  ; Remove all Files
  RmDir /r "$INSTDIR\"

  SetAutoClose false
SectionEnd

; Optionally cleans up user data/plugins
Section /o "un.User settings and plugins" UNSEC02
    SectionIn 1
    SetShellVarContext current ; Current user only
    RmDir /r "$APPDATA\${PRODUCT_NAME}" ; Remove app generated config data/plugins
    RmDir /r "$LOCALAPPDATA\${PRODUCT_NAME}" ; Remove app generated config data/plugins
SectionEnd

;Function un.onUninstSuccess
;FunctionEnd

; Description Texts for Component page
!insertmacro MUI_UNFUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${UNSEC01} "Core program files"
  !insertmacro MUI_DESCRIPTION_TEXT ${UNSEC02} "User settings and plugins"
!insertmacro MUI_UNFUNCTION_DESCRIPTION_END

;------------------------------ End Uninstaller -------------------------------
