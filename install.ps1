# Installation Script for HR Policy Assistant
# Run this in PowerShell: .\install.ps1

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "HR POLICY ASSISTANT - INSTALLATION" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check Ollama
Write-Host "`n[2/5] Checking Ollama..." -ForegroundColor Yellow
try {
    $ollamaVersion = & ollama --version 2>&1
    Write-Host "  ✓ Ollama found: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Ollama not found." -ForegroundColor Red
    Write-Host "  Please install from: https://ollama.ai" -ForegroundColor Yellow
    exit 1
}

# Pull Mistral model
Write-Host "`n[3/5] Pulling Mistral model..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray
try {
    & ollama pull mistral
    Write-Host "  ✓ Mistral model ready" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to pull model" -ForegroundColor Red
}

# Activate virtual environment
Write-Host "`n[4/5] Activating virtual environment..." -ForegroundColor Yellow
$venvPath = "H:\aiml\agentic\.venv-1\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "  ! Virtual environment not found, creating..." -ForegroundColor Yellow
    python -m venv .venv-1
    & "H:\aiml\agentic\.venv-1\Scripts\Activate.ps1"
    Write-Host "  ✓ Virtual environment created and activated" -ForegroundColor Green
}

# Install packages
Write-Host "`n[5/5] Installing Python packages..." -ForegroundColor Yellow
Write-Host "  This will take several minutes..." -ForegroundColor Gray

$packages = @(
    "langchain",
    "langchain-community",
    "ollama",
    "faiss-cpu",
    "sentence-transformers",
    "streamlit",
    "python-dotenv",
    "pydantic",
    "pypdf"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    & pip install $package --quiet
}

Write-Host "  ✓ All packages installed" -ForegroundColor Green

# Final check
Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Start Ollama: ollama serve" -ForegroundColor White
Write-Host "  2. Run the app: streamlit run app.py" -ForegroundColor White
Write-Host "  3. Open browser at: http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "To verify installation, run:" -ForegroundColor Yellow
Write-Host "  python check_system.py" -ForegroundColor White
Write-Host ""
