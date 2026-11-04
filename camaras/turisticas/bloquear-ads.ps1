# Bloquear publicidad de SkylineWebcams en OBS
# IMPORTANTE: ejecutar como Administrador (clic derecho -> Ejecutar como administrador)

$hostsFile = "$env:SystemRoot\System32\drivers\etc\hosts"
$marker = "# --- SKYLINEWEBCAMS-ADS-BLOCK ---"
$entries = @(
    "$marker",
    "0.0.0.0 googleads.g.doubleclick.net",
    "0.0.0.0 pagead2.googlesyndication.com",
    "0.0.0.0 tpc.googlesyndication.com",
    "0.0.0.0 imasdk.googleapis.com",
    "0.0.0.0 ad.skylinewebcams.com",
    "0.0.0.0 adservice.google.com",
    "0.0.0.0 adclick.g.doubleclick.net"
)

$current = Get-Content -LiteralPath $hostsFile -Raw -ErrorAction SilentlyContinue

if ($current -and $current -match [regex]::Escape($marker)) {
    Write-Host "Ya esta configurado. No se necesita nada."
} else {
    $newEntries = ($entries -join "`n") + "`n"
    Add-Content -LiteralPath $hostsFile -Value $newEntries -Encoding ASCII
    Write-Host "Listo. Dominios de publicidad bloqueados."
}

# Limpiar cache DNS para que surta efecto inmediato
ipconfig /flushdns | Out-Null
Write-Host "Cache DNS limpiada."
Write-Host ""
Write-Host "Para DESHABILITAR el bloqueo despues, ejecuta:"
Write-Host "  notepad $hostsFile"
Write-Host "y borra las lineas que empiezan con '0.0.0.0' y la linea '# --- SKYLINEWEBCAMS-ADS-BLOCK ---'"
