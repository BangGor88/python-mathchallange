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

$faceBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 243, 174))
$faceRect = New-Object System.Drawing.Rectangle 28, 28, 200, 200
$gfx.FillEllipse($faceBrush, $faceRect)

$outlinePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 46, 90, 60), 6)
$gfx.DrawEllipse($outlinePen, $faceRect)

$eyeBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 46, 90, 60))
$gfx.FillEllipse($eyeBrush, 84, 90, 22, 22)
$gfx.FillEllipse($eyeBrush, 150, 90, 22, 22)

$smilePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 46, 90, 60), 7)
$gfx.DrawArc($smilePen, 82, 105, 92, 80, 20, 140)

$font = New-Object System.Drawing.Font("Arial", 36, [System.Drawing.FontStyle]::Bold)
$textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 35, 112, 59))
$gfx.DrawString("1+2", $font, $textBrush, 72, 150)

$starBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 184, 0))
$gfx.FillPolygon($starBrush, @(
    (New-Object System.Drawing.Point 214, 30),
    (New-Object System.Drawing.Point 224, 56),
    (New-Object System.Drawing.Point 252, 58),
    (New-Object System.Drawing.Point 230, 74),
    (New-Object System.Drawing.Point 238, 100),
    (New-Object System.Drawing.Point 214, 84),
    (New-Object System.Drawing.Point 190, 100),
    (New-Object System.Drawing.Point 198, 74),
    (New-Object System.Drawing.Point 176, 58),
    (New-Object System.Drawing.Point 204, 56)
))

$icon = [System.Drawing.Icon]::FromHandle($bmp.GetHicon())
$fs = [System.IO.File]::Open($iconPath, [System.IO.FileMode]::Create)
$icon.Save($fs)
$fs.Close()

$gfx.Dispose()
$bgBrush.Dispose()
$faceBrush.Dispose()
$outlinePen.Dispose()
$eyeBrush.Dispose()
$smilePen.Dispose()
$font.Dispose()
$textBrush.Dispose()
$starBrush.Dispose()
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
