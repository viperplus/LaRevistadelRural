$ErrorActionPreference = "Continue"

$outDir = Join-Path $PSScriptRoot "turisticas"
$template = Get-Content -LiteralPath (Join-Path $outDir "cam-torreon-mar-del-plata.html") -Raw
$template = $template.Replace("Torreon - Mar del Plata", "__TITLE__").Replace("https://video5.estadodelmar.com.ar/mobile/TORREON/index.m3u8", "__URL__")

function Get-PrettyName([string]$slug) {
  return ($slug -split "-" | ForEach-Object { $_.Substring(0,1).ToUpper() + $_.Substring(1) }) -join " "
}

$retry = @(
  "acantilados","bahia-faro","balneario-cero","cardiel","chapadmalal-4","el-barco",
  "honu-beach","horizonte-del-sol","paradise","varese","waikiki"
)

# Streams conocidos pero caidos en este momento: generar igual (reconectan solos)
$knownDown = @{
  "sun-rider"           = "https://video.estadodelmar.com.ar/mobile/SUNRIDER/index.m3u8"
  "windy-villa-gesell"  = "https://video.estadodelmar.com.ar/mobile/vgesell/index.m3u8"
}
foreach ($k in $knownDown.Keys) {
  $content = $template.Replace("__TITLE__", (Get-PrettyName $k)).Replace("__URL__", $knownDown[$k])
  Set-Content -LiteralPath (Join-Path $outDir "cam-$k.html") -Value $content -Encoding UTF8
  Write-Host "GENERADA (offline ahora) $k"
}

foreach ($slug in $retry) {
  Start-Sleep -Seconds 3
  $player = $null; $m3u8 = $null; $status = ""

  for ($i = 0; $i -lt 3; $i++) {
    try {
      $c = (Invoke-WebRequest -Uri "https://estadodelmar.com.ar/camaras/$slug/" -UseBasicParsing -TimeoutSec 40).Content
      $player = ($c | Select-String -Pattern 'iframe[^>]*src="(https://video[^"]+)"' -AllMatches).Matches |
        ForEach-Object { $_.Groups[1].Value } | Select-Object -First 1
      if ($player) { break }
      Start-Sleep -Seconds 2
    } catch { Start-Sleep -Seconds 5 }
  }

  if (-not $player) { Write-Host "SIN_PLAYER    $slug"; continue }

  try {
    $pc = (Invoke-WebRequest -Uri $player -UseBasicParsing -TimeoutSec 30).Content
    $m3u8 = ($pc | Select-String -Pattern 'https?://[^"'' ]+\.m3u8[^"'' ]*' -AllMatches).Matches |
      ForEach-Object { $_.Value } | Select-Object -Unique -First 1
  } catch { }

  if ($m3u8) {
    try {
      $r = Invoke-WebRequest -Uri $m3u8 -UseBasicParsing -TimeoutSec 25
      if ($r.StatusCode -eq 200) {
        $content = $template.Replace("__TITLE__", (Get-PrettyName $slug)).Replace("__URL__", $m3u8)
        Set-Content -LiteralPath (Join-Path $outDir "cam-$slug.html") -Value $content -Encoding UTF8
        Write-Host "OK            $slug"
        continue
      }
    } catch { }
    # Generar igual: el stream puede volver a estar online mas tarde
    $content = $template.Replace("__TITLE__", (Get-PrettyName $slug)).Replace("__URL__", $m3u8)
    Set-Content -LiteralPath (Join-Path $outDir "cam-$slug.html") -Value $content -Encoding UTF8
    Write-Host "GENERADA (offline ahora) $slug -> $m3u8"
  } else {
    Write-Host "NO_M3U8       $slug ($player)"
  }
}
