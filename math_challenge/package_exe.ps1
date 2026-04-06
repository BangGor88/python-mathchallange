$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

$venvPython = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Python virtual environment not found at ..\.venv\Scripts\python.exe"
}

$assetsDir = Join-Path $PSScriptRoot "build_assets"
New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null
$iconPath = Join-Path $assetsDir "math_challenge_icon.ico"

Add-Type -AssemblyName System.Drawing

$size = 256
$bmp = New-Object System.Drawing.Bitmap $size, $size
$gfx = [System.Drawing.Graphics]::FromImage($bmp)
$gfx.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

$rect = New-Object System.Drawing.Rectangle 0, 0, $size, $size
$bgBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
    $rect,
    [System.Drawing.Color]::FromArgb(255, 192, 245, 206),
    [System.Drawing.Color]::FromArgb(255, 122, 194, 138),
    45
)
$gfx.FillRectangle($bgBrush, $rect)

$framePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 77, 50, 35), 14)
$rodPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 125, 83, 56), 8)
$abacusFill = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 240, 222, 195))

$frameRect = New-Object System.Drawing.Rectangle 28, 26, 200, 204
$gfx.FillRectangle($abacusFill, $frameRect)
$gfx.DrawRectangle($framePen, $frameRect)

$beadPalette = @(
    [System.Drawing.Color]::FromArgb(255, 255, 99, 132),
    [System.Drawing.Color]::FromArgb(255, 255, 159, 67),
    [System.Drawing.Color]::FromArgb(255, 255, 206, 84),
    [System.Drawing.Color]::FromArgb(255, 72, 219, 251),
    [System.Drawing.Color]::FromArgb(255, 29, 209, 161)
)

$rowYs = @(60, 92, 124, 156, 188)
$beadXs = @(56, 82, 108, 134, 160, 186)

for ($r = 0; $r -lt $rowYs.Count; $r++) {
    $y = [int]$rowYs[$r]
    $gfx.DrawLine($rodPen, 42, $y, 214, $y)

    for ($b = 0; $b -lt $beadXs.Count; $b++) {
        $x = [int]$beadXs[$b]
        $paletteIndex = ($r + $b) % $beadPalette.Count
        $beadBrush = New-Object System.Drawing.SolidBrush($beadPalette[$paletteIndex])
        $beadShadePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 110, 73, 49), 2)
        $gfx.FillEllipse($beadBrush, $x - 10, $y - 12, 20, 24)
        $gfx.DrawEllipse($beadShadePen, $x - 10, $y - 12, 20, 24)
        $beadBrush.Dispose()
        $beadShadePen.Dispose()
    }
}

$sparkBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220, 255, 255, 255))
$gfx.FillEllipse($sparkBrush, 34, 32, 10, 10)
$gfx.FillEllipse($sparkBrush, 214, 214, 10, 10)

$icon = [System.Drawing.Icon]::FromHandle($bmp.GetHicon())
$fs = [System.IO.File]::Open($iconPath, [System.IO.FileMode]::Create)
$icon.Save($fs)
$fs.Close()

$gfx.Dispose()
$bgBrush.Dispose()
$framePen.Dispose()
$rodPen.Dispose()
$abacusFill.Dispose()
$sparkBrush.Dispose()
$icon.Dispose()
$bmp.Dispose()

& $venvPython -m pip install pyinstaller

& $venvPython -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name MathChallenge `
    --icon $iconPath `
    main.py

Write-Host "Build complete. Executable: dist\MathChallenge.exe"
