$ErrorActionPreference = 'Stop'
$ruleName = 'FaceDoor Python UDP 9090-9091'
$program = 'C:\Users\守护者\Desktop\Face-door-master\.venv\Scripts\python.exe'
$result = 'C:\Users\守护者\Desktop\Face-door-master\tools\firewall_result.txt'
try {
    $existing = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
    if ($existing) {
        Set-NetFirewallRule -DisplayName $ruleName -Enabled True -Action Allow
    } else {
        New-NetFirewallRule -DisplayName $ruleName -Description 'Allow FaceDoor Python to receive ESP32-CAM images' -Direction Inbound -Action Allow -Protocol UDP -LocalPort 9090,9091 -Program $program -Profile Private,Public -Enabled True | Out-Null
    }
    'OK' | Set-Content -LiteralPath $result -Encoding ascii
} catch {
    ($_ | Out-String) | Set-Content -LiteralPath $result -Encoding utf8
    exit 1
}