$ErrorActionPreference='Stop'
$dev = Get-PnpDevice -PresentOnly | Where-Object { $_.Class -eq 'Ports' -and $_.FriendlyName -match 'CH340' } | Select-Object -First 1
if (-not $dev) { throw '没有找到 CH340 串口设备' }
pnputil /restart-device "$($dev.InstanceId)"
Start-Sleep -Seconds 3
.\.venv\Scripts\python.exe -c "import serial.tools.list_ports as p; print('CH340:', [x.device for x in p.comports() if 'CH340' in (x.description or '')])"