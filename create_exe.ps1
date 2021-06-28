# Powershell5では動かせないようにする
if(!($PSVersionTable["PSCompatibleVersions"].Major -contains 6)){
  Write-Host @'
    This script must be PowerShell version 6 or higher before it will work properly.
    The shell currently running is PowerShell version 5 or lower.
    Use the `pwsh` command to change to PowerShell 6.
'@
  exit
}
$appshortname = "SBCLinkCopyTool"
if (Test-Path dist) {
  Remove-Item dist -Recurse | Out-Null
}
New-Item dist -ItemType Directory | Out-Null
# windllを捜索
Write-Host "> Searching WinDLL"
$windll = "c:\windows\WinSxS\x86_microsoft-windows-m..namespace-downlevel_*"
$windllpath = "."
if(Test-Path $windll){
  $item = (Get-ChildItem $windll | Sort-Object LastWriteTime)[0]
  $windllpath = '"c:\windows\WinSxS\{0}"' -f $item.Name
}
# pyinstaller
Write-Host "> Creation EXE"
pyinstaller `
  --name $appshortname `
  --windowed `
  --path $windllpath `
  --path C:/Windows/System32/downlevel `
  --specpath ./dist/ `
  --distpath ./dist/dist `
  --workpath ./dist/build `
  --add-data "../config.yaml;." `
  main.py
if(Test-Path ".\dist\dist\$appshortname"){
  Remove-Item ./dist/dist/$appshortname/package*.json
}