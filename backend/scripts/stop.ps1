# Stop eventlens - PowerShell version
Write-Host "🛑 Stopping eventlens..." -ForegroundColor Yellow

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ eventlens stopped successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to stop services!" -ForegroundColor Red
}