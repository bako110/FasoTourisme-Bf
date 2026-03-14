# Script de configuration des secrets Fly.io pour Tourisme Burkina API
# Exécutez ce script : .\deploy-secrets.ps1

Write-Host "Configuration des secrets Fly.io..." -ForegroundColor Green

# Générer une clé secrète sécurisée pour JWT
Write-Host "`n1. Génération de SECRET_KEY..." -ForegroundColor Yellow
$secretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
Write-Host "SECRET_KEY généré: $secretKey" -ForegroundColor Cyan

# Configuration de tous les secrets
Write-Host "`n2. Configuration de MONGODB_URL..." -ForegroundColor Yellow
fly secrets set MONGODB_URL="mongodb+srv://bakorobert2000:1jHcf2qX4D53KHyw@cluster0.hfr2vqx.mongodb.net/tourisme_burkina?retryWrites=true&w=majority&appName=Cluster0" SECRET_KEY="$secretKey" ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8080,https://tourisme-burkina-api.fly.dev,*"

Write-Host "`n✅ Tous les secrets sont configurés!" -ForegroundColor Green
Write-Host "`nPour déployer maintenant, exécutez:" -ForegroundColor Cyan
Write-Host "  fly deploy" -ForegroundColor White
