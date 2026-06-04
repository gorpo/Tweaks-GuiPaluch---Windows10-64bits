$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$PythonRoot = Split-Path -Parent (python -c "import sys; print(sys.executable)")
$TclRoot = Join-Path $PythonRoot "tcl"
$DllRoot = Join-Path $PythonRoot "DLLs"
$env:TCL_LIBRARY = Join-Path $TclRoot "tcl8.6"
$env:TK_LIBRARY = Join-Path $TclRoot "tk8.6"

python -m PyInstaller `
  --additional-hooks-dir "pyinstaller_hooks" `
  --onefile `
  --noconsole `
  --uac-admin `
  --name "Tweaks GuiPaluch" `
  --icon "tweaks_guipaluch.ico" `
  --add-data "tweaks_guipaluch.ico;." `
  --add-data "$TclRoot\tcl8.6;_tcl_data" `
  --add-data "$TclRoot\tk8.6;_tk_data" `
  --add-data "$TclRoot\tcl8;tcl\tcl8" `
  --add-binary "$DllRoot\tcl86t.dll;." `
  --add-binary "$DllRoot\tk86t.dll;." `
  --add-binary "$DllRoot\_tkinter.pyd;." `
  --hidden-import "tkinter" `
  --hidden-import "tkinter.ttk" `
  --clean `
  "tweaks_gui.py"

Write-Host ""
Write-Host "Executavel gerado em:"
Write-Host (Join-Path $Root "dist\Tweaks GuiPaluch.exe")
