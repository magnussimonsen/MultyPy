# Build script for creating MultiPy.exe
# Run this script to build the Windows executable

Write-Host "=== MultiPy Build Script ===" -ForegroundColor Green
Write-Host ""

# Check if pyinstaller is installed
Write-Host "Checking for PyInstaller..." -ForegroundColor Yellow
try {
    python -c "import PyInstaller" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
        pip install pyinstaller
    } else {
        Write-Host "PyInstaller is already installed." -ForegroundColor Green
    }
} catch {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

Write-Host ""
Write-Host "Building MultiPy.exe..." -ForegroundColor Yellow
Write-Host ""

# Run PyInstaller
# Note: Since MultiPy.spec might not exist yet, we'll use a basic command first.
# If you create a spec file later, change this line to: pyinstaller --clean --noconfirm MultiPy.spec
pyinstaller --clean --noconfirm --name MultiPy --onefile --windowed run.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Build Complete! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your executable is located at:" -ForegroundColor Cyan
    Write-Host "  dist\MultiPy.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "To run the app:" -ForegroundColor Yellow
    Write-Host "  .\dist\MultiPy.exe" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "Build failed! Check the error messages above." -ForegroundColor Red
}
