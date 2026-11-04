$ErrorActionPreference = "Continue"

$outDir = Join-Path $PSScriptRoot "turisticas"
$template = Get-Content -LiteralPath (Join-Path $outDir "cam-torreon-mar-del-plata.html") -Raw
$template = $template.Replace("Torreon - Mar del Plata", "__TITLE__").Replace("https://video5.estadodelmar.com.ar/mobile/TORREON/index.m3u8", "__URL__")

function Get-PrettyName([string]$slug) {
  return ($slug -split "-" | ForEach-Object { $_.Substring(0,1).ToUpper() + $_.Substring(1) }) -join " "
}

$retry = @(
  "acantilados","bahia-faro","balneario-cero","cardiel","chapadmalal-4","el-barco",
  "honu-beach","horizonte-del-sol","paradise","varese","waikiki",
  "hemingway","la-pepita","playa-pura-vida","sun-rider","windy-villa-gesell"
)

foreach ($slug in $retry) {
  Start-Sleep -Seconds 1
  $player = $null; $m3u8 = $null; $status = ""

  try {
    $c = (Invoke-WebRequest -Uri "https://estadodelmar.com.ar/camaras/$slug/" -UseBasicParsing -TimeoutSec 40).Content
    $player = ($c | Select-String -Pattern 'iframe[^>]*src="(https://video[^"]+)"' -AllMatches).Matches |
      ForEach-Object { $_.Groups[1].Value } | Select-Object -First 1
    if (-not $player) {
      $yt = ($c | Select-String -Pattern '(?:youtube\.com/embed/|youtu\.be/)([\w-]{11})' -AllMatches).Matches |
        ForEach-Object { $_.Groups[1].Value } | Select-Object -First 1
      if ($yt) { Write-Host "YOUTUBE       $slug -> $yt"; continue }
    }
  } catch { $status = "PAGE_ERR" }

  if ($player) {
    try {
      $pc = (Invoke-WebRequest -Uri $player -UseBasicParsing -TimeoutSec 30).Content
      $m3u8 = ($pc | Select-String -Pattern 'https?://[^"'' ]+\.m3u8[^"'' ]*' -AllMatches).Matches |
        ForEach-Object { $_.Value } | Select-Object -Unique -First 1
    } catch { $status = "PLAYER_ERR" }
  }

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
    Write-Host "STREAM_DOWN   $slug -> $m3u8"
  } else {
    Write-Host "$($status.PadRight(13)) $slug"
  }
}
