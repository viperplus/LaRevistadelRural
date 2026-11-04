$ErrorActionPreference = "Continue"

$slugs = @(
  "acantilados","alicante","bahia-faro","balneario-cero","caleta-olivia-nautico",
  "california","camet-norte","cardiel","chapadmalal","chapadmalal-4","chapadmalal-5",
  "daprotis","el-barco","el-chiringo","el-muelle","el-nautico","el-torreon","el-yacht",
  "hemingway","honores-viento-norte","honu-beach","honu-beach-norte","horizonte-del-sol",
  "hotel-guerrero","indo-bar-costa-corvinas","la-40","la-martina","la-nativa",
  "la-normandina","la-pepita","las-grutas","las-toninas","luna-roja","mar-de-ajo-nias",
  "mar-de-ajo-sunset","mariano","mirasoles-el-muelle","paradise","playa-grande",
  "playa-pura-vida","playa-serena-2","rambla-ostende","san-bernardo-bottom",
  "santa-teresita","santa-teresita-camping-estancia","sun-rider","torreon-del-monje",
  "valeria-del-mar-la-pergola","varese","waikiki","waikiki-club-de-surf","waimea",
  "windy-villa-gesell"
)

$outDir = Join-Path $PSScriptRoot "turisticas"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

# Template HLS basado en el archivo ya generado de Torreon
$template = Get-Content -LiteralPath (Join-Path $outDir "cam-torreon-mar-del-plata.html") -Raw
$template = $template.Replace("Torreon - Mar del Plata", "__TITLE__").Replace("https://video5.estadodelmar.com.ar/mobile/TORREON/index.m3u8", "__URL__")

function Get-PrettyName([string]$slug) {
  return ($slug -split "-" | ForEach-Object { $_.Substring(0,1).ToUpper() + $_.Substring(1) }) -join " "
}

$results = New-Object System.Collections.Generic.List[object]

foreach ($slug in $slugs) {
  $pageUrl = "https://estadodelmar.com.ar/camaras/$slug/"
  $player = $null; $m3u8 = $null; $yt = $null; $status = ""

  try {
    $c = (Invoke-WebRequest -Uri $pageUrl -UseBasicParsing -TimeoutSec 20).Content
    $player = ($c | Select-String -Pattern 'iframe[^>]*src="(https://video[^"]+)"' -AllMatches).Matches |
      ForEach-Object { $_.Groups[1].Value } | Select-Object -First 1
    if (-not $player) {
      $yt = ($c | Select-String -Pattern '(?:youtube\.com/embed/|youtu\.be/)([\w-]{11})' -AllMatches).Matches |
        ForEach-Object { $_.Groups[1].Value } | Select-Object -First 1
    }
    Start-Sleep -Milliseconds 200
  } catch {
    $status = "PAGE_ERR"
  }

  if ($player) {
    try {
      $pc = (Invoke-WebRequest -Uri $player -UseBasicParsing -TimeoutSec 20).Content
      $m3u8 = ($pc | Select-String -Pattern 'https?://[^"'' ]+\.m3u8[^"'' ]*' -AllMatches).Matches |
        ForEach-Object { $_.Value } | Select-Object -Unique -First 1
      Start-Sleep -Milliseconds 200
    } catch {
      $status = "PLAYER_ERR"
    }
  }

  if ($m3u8) {
    try {
      $r = Invoke-WebRequest -Uri $m3u8 -UseBasicParsing -TimeoutSec 15
      if ($r.StatusCode -eq 200) {
        $status = "OK"
        $title = Get-PrettyName $slug
        $content = $template.Replace("__TITLE__", $title).Replace("__URL__", $m3u8)
        $file = "cam-$slug.html"
        Set-Content -LiteralPath (Join-Path $outDir $file) -Value $content -Encoding UTF8
      } else { $status = "HTTP_$($r.StatusCode)" }
    } catch {
      $status = "STREAM_DOWN"
    }
  }
  elseif ($yt) { $status = "YOUTUBE:$yt" }
  elseif (-not $status) { $status = "NO_PLAYER" }

  $results += [pscustomobject]@{ slug = $slug; status = $status; m3u8 = $m3u8 }
  Write-Host "$($status.PadRight(12)) $slug"
}

Write-Host "`n===== RESUMEN ====="
$ok = $results | Where-Object { $_.status -eq "OK" }
Write-Host "Generadas OK: $($ok.Count) de $($slugs.Count)"
$results | Export-Csv -LiteralPath (Join-Path $PSScriptRoot "reporte-camaras.csv") -NoTypeInformation -Encoding UTF8

# YouTube embeds encontrados
foreach ($r in ($results | Where-Object { $_.status -like "YOUTUBE:*" })) {
  Write-Host "YouTube: $($r.slug) -> $($r.status)"
}
