$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

python -m PyInstaller `
  --onefile `
  --noconsole `
  --uac-admin `
  --name "Tweaks GuiPaluch" `
  --icon "tweaks_guipaluch.ico" `
  --add-data "tweaks_guipaluch.ico;." `
  --clean `
  "tweaks_gui.py"

Write-Host ""
Write-Host "Executavel gerado em:"
Write-Host (Join-Path $Root "dist\Tweaks GuiPaluch.exe")
