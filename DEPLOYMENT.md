# Guide de Déploiement sur Fly.io

## Prérequis

1. Installer Fly CLI:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. Se connecter à Fly.io:
   ```bash
   fly auth login
   ```

## Étapes de Déploiement

### 1. Configuration de MongoDB

Vous avez deux options pour MongoDB:

#### Option A: MongoDB Atlas (Recommandé)
1. Créez un cluster gratuit sur [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Obtenez votre URL de connexion
3. Autorisez les connexions depuis n'importe quelle IP (0.0.0.0/0) dans Atlas

#### Option B: MongoDB sur Fly.io
```bash
# Créez une application MongoDB sur Fly
fly apps create tourisme-burkina-mongodb
```

### 2. Créer l'application Fly.io

```bash
# Depuis le dossier backend
fly apps create tourisme-burkina-api
```

### 3. Configurer les secrets

```bash
# MongoDB URL (Atlas ou votre propre instance)
fly secrets set MONGODB_URL="mongodb+srv://username:password@cluster.mongodb.net/tourisme_burkina?retryWrites=true&w=majority"

# Générer une clé secrète sécurisée pour JWT
fly secrets set SECRET_KEY="$(openssl rand -hex 32)"

# CORS Origins (ajoutez vos domaines de production)
fly secrets set ALLOWED_ORIGINS="https://votre-domaine.com,https://www.votre-domaine.com"
```

### 4. Déployer l'application

```bash
# Premier déploiement
fly deploy

# Déploiements suivants
fly deploy
```

### 5. Vérifier le déploiement

```bash
# Vérifier le statut
fly status

# Voir les logs
fly logs

# Ouvrir l'application dans le navigateur
fly open

# Tester l'API
fly open /health
fly open /api/docs
```

## Configuration Avancée

### Scaling

```bash
# Augmenter la mémoire
fly scale memory 512

# Augmenter le nombre de machines
fly scale count 2

# Changer la région
fly regions add cdg  # Paris
fly regions add jnb  # Johannesburg
```

### Variables d'environnement

Pour modifier les variables d'environnement publiques, éditez `fly.toml` puis redéployez:

```bash
fly deploy
```

Pour les secrets (données sensibles):

```bash
fly secrets set MY_SECRET="secret_value"
```

### Monitoring

```bash
# Voir les métriques
fly dashboard

# Voir les logs en temps réel
fly logs -f

# Se connecter à la machine via SSH
fly ssh console
```

## Coûts Estimés

- **Plan Gratuit Fly.io**: Inclut assez de ressources pour un petit projet
  - 3 machines partagées 1x
  - 160GB de trafic sortant
  
- **MongoDB Atlas**: Cluster gratuit M0 avec 512MB de stockage

## Domaine Personnalisé

```bash
# Ajouter un certificat SSL automatique
fly certs add votre-domaine.com

# Obtenir les instructions DNS
fly certs show votre-domaine.com
```

Puis configurez votre DNS avec les valeurs fournies.

## Rollback en cas de problème

```bash
# Lister les versions
fly releases

# Revenir à la version précédente
fly releases rollback
```

## Support et Dépannage

### Problèmes communs

1. **L'application ne démarre pas**
   - Vérifiez les logs: `fly logs`
   - Vérifiez que MONGODB_URL est bien configuré: `fly secrets list`

2. **Erreur de connexion MongoDB**
   - Vérifiez que votre IP est autorisée dans MongoDB Atlas
   - Testez la connexion MongoDB depuis la console: `fly ssh console`

3. **API lente**
   - Considérez augmenter la mémoire: `fly scale memory 512`
   - Ajoutez des régions supplémentaires pour être plus proche des utilisateurs

### Commandes utiles

```bash
# Redémarrer l'application
fly apps restart tourisme-burkina-api

# Détruire l'application (attention!)
fly apps destroy tourisme-burkina-api

# Voir toutes les applications
fly apps list
```

## Sécurité

- ✅ Les secrets sont chiffrés
- ✅ HTTPS forcé par défaut
- ✅ L'application tourne avec un utilisateur non-root
- ✅ Debug désactivé en production
- ⚠️ N'oubliez pas de restreindre ALLOWED_ORIGINS en production

## Next Steps

Après le déploiement:

1. Configurez votre domaine personnalisé
2. Ajoutez un service de monitoring (Sentry, etc.)
3. Configurez des backups pour MongoDB
4. Mettez en place un CI/CD avec GitHub Actions
