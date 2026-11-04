# Regenera los 75 audios usando la mejor voz argentina disponible.
# Uso:  powershell -NoProfile -ExecutionPolicy Bypass -File generar-audio-arg.wav.ps1
Add-Type -AssemblyName System.Speech

$proyecto = 'C:\Users\black\Desktop\opencode archivos\clase n°4'
$origen   = Join-Path $proyecto 'FRASES-PARA-AUDIO.txt'
$destino  = Join-Path $proyecto 'audio'

if (-not (Test-Path -LiteralPath $destino)) {
  New-Item -ItemType Directory -Path $destino -Force | Out-Null
}

# --- busca la mejor voz argentina; si no hay, avisa y NO genera nada ---
$s = [System.Speech.Synthesis.SpeechSynthesizer]::new()
$todas = @($s.GetInstalledVoices() | Where-Object { $_.Enabled } | ForEach-Object { $_.VoiceInfo })

$ar = @($todas | Where-Object { $_.Culture.Name -eq 'es-AR' })
if ($ar.Count -eq 0) {
  Write-Output 'ERROR: no hay ninguna voz es-AR instalada.'
  Write-Output ''
  Write-Output 'Instalala en:  Configuracion > Tiempo e idioma > Voz > Agregar voces > Espanol (Argentina)'
  Write-Output ''
  Write-Output 'Voces de espanol que si tenes:'
  $todas | Where-Object { $_.Culture.Name -like 'es*' } |
    ForEach-Object { Write-Output ('  ' + $_.Name + '  (' + $_.Culture.Name + ')') }
  $s.Dispose()
  exit 1
}

# entre las argentinas, la mejor es la que dice natural/online/neural
$voz = ($ar | Where-Object { $_.Name -match 'natural|online|neural|enhanced|premium' } | Select-Object -First 1)
if (-not $voz) { $voz = $ar[0] }
Write-Output ('Voz elegida: ' + $voz.Name + '  (' + $voz.Culture.Name + ')')
Write-Output ''

$rate = -2
$volumen = 100
$s.SelectVoice($voz.Name)

function Limpiar-Texto([string]$t) {
  $t = $t -replace '[\uD800-\uDBFF][\uDC00-\uDFFF]', ''
  $t = [regex]::Replace($t, '[\p{So}\p{Cf}\p{Cs}]', '')
  $t = $t -replace '[\u2700-\u27BF]', ''
  $t = $t -replace '[\u2B00-\u2BFF]', ''
  $t = $t -replace '\s+', ' '
  return $t.Trim()
}

$vistos = @{}
$lista  = New-Object System.Collections.Generic.List[string]
$hechas = 0
$fallos = 0

foreach ($linea in [System.IO.File]::ReadAllLines($origen, [System.Text.UTF8Encoding]::new($false))) {
  if (-not $linea -or $linea.StartsWith('#')) { continue }
  $partes = $linea -split '\|', 4
  if ($partes.Count -lt 4) { continue }

  $num   = $partes[0].Trim()
  $clave = $partes[1].Trim()
  $tipo  = $partes[2].Trim()
  $texto = Limpiar-Texto $partes[3]
  if (-not $texto) { continue }

  $nombre = $clave
  if ($vistos.ContainsKey($nombre)) {
    $vistos[$nombre]++
    $nombre = $clave + '_' + $vistos[$nombre]
  } else { $vistos[$clave] = 1 }
  $archivo = Join-Path $destino ($nombre + '.wav')

  try {
    $s.Rate = $rate
    $s.Volume = $volumen
    $s.SetOutputToWaveFile($archivo)
    $s.Speak($texto)
    $s.SetOutputToNull()
    $hechos++
    $lista.Add(("{0,3}  {1,-34} {2,-16} {3}" -f $num, $nombre, $tipo, $texto))
  } catch {
    $fallos++
    $lista.Add(("{0,3}  {1,-34} {2,-16} FALLO: {3}" -f $num, $nombre, $tipo, $_.Exception.Message))
  }
}
$s.Dispose()

$indice = @('# AUDIOS - ' + $voz.Name + ' (' + $voz.Culture.Name + '), velocidad ' + $rate, '')
$indice += $lista
$indice += ''
$indice += ('# generados: {0}   fallos: {1}' -f $hechos, $fallos)
[System.IO.File]::WriteAllLines((Join-Path $destino '_INDICE.txt'), $indice, [System.Text.UTF8Encoding]::new($false))

Write-Output ('generados: ' + $hechos + '   fallos: ' + $fallos)
