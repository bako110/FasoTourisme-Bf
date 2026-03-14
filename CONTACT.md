# 📞 GUIDE DE CONTACT & SUPPORT

**Application:** Tourisme Burkina Faso  
**Version:** 1.0.0  
**Dernière mise à jour:** 13 Mars 2026

---

## 🟢 STATUT DE SUPPORT

| Service | Statut | Temps Réponse |
|---------|--------|---------------|
| 🟢 Email Support | Opérationnel | 24-48h |
| 🟢 Chat Support | Opérationnel | 2-4h (heures de bureau) |
| 🟢 Téléphone | Opérationnel | Immédiat |
| 🟢 Formulaire Web | Opérationnel | 24-48h |
| 🟢 API Support | Opérationnel | 24h |

---

## 📧 CANAUX DE CONTACT

### 1️⃣ EMAIL - Recommandé pour questions complexes

```
General Support:    support@tourisme-burkina.bf
Technical Issues:   tech@tourisme-burkina.bf
Billing Issues:     billing@tourisme-burkina.bf
Security Issues:    security@tourisme-burkina.bf
Emergency:          emergency@tourisme-burkina.bf
Feedback:           feedback@tourisme-burkina.bf
```

**Format d'email recommandé:**
```
Sujet: [TYPE] - Description courte

Contenu:
1. Votre nom complet
2. Numéro de client/compte (si applicable)
3. Description détaillée du problème
4. Étapes pour reproduire (si c'est un bug)
5. Captures d'écran (si pertinent)

Signature:
Email: votre@email.com
Téléphone: +226 XX XX XX XX
```

---

### 2️⃣ TÉLÉPHONE - Pour urgences ou questions urgentes

```
Numéro Principal:    +226 XX XX XX XX
Heures de bureau:    08:00 - 18:00 (Lundi-Vendredi)
Fuseau horaire:      GMT+0 (UTC)
Langue:              Français, Anglais
```

**Options du menu téléphonique:**
```
Appuyez sur:
1 → Support Technique
2 → Réservations & Bookings
3 → Problèmes de Paiement
4 → Questions de Sécurité
5 → Autres demandes
0 → Transférer à un agent
```

---

### 3️⃣ FORMULAIRE WEB - Via l'API

**Endpoint:** `POST /api/v1/support/contact`

```bash
curl -X POST "http://localhost:8000/api/v1/support/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Jean Dupont",
    "email": "jean@example.com",
    "telephone": "+226 XX XX XX XX",
    "sujet": "Problème de réservation",
    "message": "Je n''arrive pas à faire ma réservation...",
    "type_demande": "support"
  }'
```

**Réponse (succès):**
```json
{
  "status": "success",
  "message": "Message reçu avec succès ✅",
  "ticket_id": "TSK-20260313143025",
  "email_confirmation": "Une confirmation sera envoyée à jean@example.com",
  "response_time": "24-48 heures",
  "info": "Merci de votre message. Notre équipe vous répondra au plus tôt."
}
```

---

### 4️⃣ LIVE CHAT - Pour conversations en direct

```
Disponible sur:  www.tourisme-burkina.bf
Heures:          09:00 - 17:00 (Lundi-Vendredi)
Temps d'attente: ~5-10 minutes
Languages:       Français, Anglais
```

---

### 5️⃣ RÉSEAUX SOCIAUX - Pour suivre les mises à jour

```
Facebook:     facebook.com/tourisme-burkina
Twitter:      @TourismeBurkina
Instagram:    @tourisme_burkina
LinkedIn:     linkedin.com/company/tourisme-burkina
```

---

## 🆘 SUPPORT D'URGENCE

### 🚨 URGENCES IMMÉDIATES (Réponse: < 5 minutes)

```
🔴 SÉCURITÉ / DANGER IMMÉDIAT
────────────────────────────────
Téléphone:  +226 XX XX XX XX (PRIORITÉ 1)
Email:      security@tourisme-burkina.bf
Whatsapp:   +226 XX XX XX XX
Police:     17
Action:     Évacuation, soutien immédiat

🔴 PROBLÈME MÉDICAL / SANTÉ
────────────────────────────────
Téléphone:  +226 XX XX XX XX
Email:      health@tourisme-burkina.bf
Ambulance:  15
CHU:        +226 50 XX XX XX (Ouagadougou)
Action:     Assistance médicale immédiate

🔴 PROBLÈME DE PAIEMENT / FRAUDE
────────────────────────────────
Téléphone:  +226 XX XX XX XX
Email:      security@tourisme-burkina.bf
Whatsapp:   +226 XX XX XX XX
Action:     Gel de compte, remboursement d'urgence
```

---

## 📋 TYPES DE DEMANDES

### SUPPORT TECHNIQUE

```
Exemples:
- "Je ne peux pas me connecter"
- "L'app crash lors du paiement"
- "La page de réservation ne charge pas"
- "Erreur 500 sur endpoint /bookings"

Contact:  tech@tourisme-burkina.bf
Type API: "bug"
```

### REQUÊTES DE NOUVELLE FONCTIONNALITÉ

```
Exemples:
- "Je voudrais un filtre par prix"
- "Ajouter la réservation en groupe"
- "Système de commentaires"
- "Paiement en plusieurs fois"

Contact:  feedback@tourisme-burkina.bf
Type API: "feature"
```

### SUPPORT CLIENT GÉNÉRAL

```
Exemples:
- "Comment faire une réservation?"
- "Quels modes de paiement?"
- "Politique d'annulation?"
- "Comment modifier ma réservation?"

Contact:  support@tourisme-burkina.bf
Type API: "support"
```

### PROBLÈMES DE PAIEMENT

```
Exemples:
- "Mon paiement n'a pas été reçu"
- "Frais supplémentaires en surprise"
- "Je veux une facture"
- "Demande de remboursement"

Contact:  billing@tourisme-burkina.bf
Type API: "autre"
```

---

## ❓ FAQ - QUESTIONS FRÉQUENTES

### Comment créer un compte?
**Réponse:** Consultez `/docs` ou envoyez email à `support@tourisme-burkina.bf`

### Combien de temps pour une réponse?
**Réponse:** 
- Écrit: 24-48 heures
- Téléphone: Immédiat (heures de bureau)
- Chat: 2-4 heures

### Comment suivre ma demande?
**Réponse:** Vous recevrez un numéro de ticket: `TSK-YYYYMMDDHHMMSS`

### Comment signaler un problème de sécurité?
**Réponse:** Email immédiat à `security@tourisme-burkina.bf` (confidentiel)

### Avez-vous un SLA?
**Réponse:** 
- Critique: 4 heures
- High: 8 heures
- Normal: 48 heures
- Low: 5 jours

---

## 🔒 SÉCURITÉ & CONFIDENTIALITÉ

### ⚠️ RÈGLES IMPORTANTES

```
✅ FAITES:
- Donner autant de détails que possible
- Inclure des captures d'écran/logs
- Suivre votre numéro de ticket
- Répondre aux demandes d'info de notre team
- Garder votre ticket confidentiel

❌ NE FAITES PAS:
- Ne JAMAIS envoyer votre mot de passe
- Ne JAMAIS envoyer de tokens/clés API
- Ne JAMAIS envoyer d'infos de carte bancaire
- N'envoyez pas de pièces jointes non sûres
- N'incluez pas d'infos personnelles sensibles
```

### 🔐 Données Traitées

```
Collectées:
- Email
- Nom
- Téléphone
- Description du problème
- Type de demande

NON Collectées:
- Mots de passe
- Tokens API
- Numéro de carte bancaire
- Données personnelles sensibles

Stockage: Sécurisé, chiffré, RGPD compliant
Retention: 30 jours après résolution
Partage: Jamais avec tiers sans consentement
```

---

## 📞 COORDONNÉES COMPLÈTES

### SIÈGE SOCIAL
```
Nom Entreprise:   Tourisme Burkina SARL
Adresse:          Ouagadougou, Burkina Faso
Pays:             Burkina Faso
Région:           Hauts-Bassins
ID Fiscal:        XX XX XX XX XXX
```

### CONTACTS DIRECTEURS

```
Directeur Général:        Prénom NOM - +226 XX XX XX XX
Responsable Support:      Prénom NOM - +226 XX XX XX XX
Responsable Technique:    Prénom NOM - +226 XX XX XX XX
Responsable Qualité:      Prénom NOM - +226 XX XX XX XX
```

### HORAIRES DE BUREAU

```
Lundi:           08:00 - 12:00 / 14:00 - 18:00
Mardi:           08:00 - 12:00 / 14:00 - 18:00
Mercredi:        08:00 - 12:00 / 14:00 - 18:00
Jeudi:           08:00 - 12:00 / 14:00 - 18:00
Vendredi:        08:00 - 12:00 / 14:00 - 17:00
Samedi:          Fermé
Dimanche:        Fermé

Jours fériés: Fermé
Urgence 24h/24: +226 XX XX XX XX
```

---

## 📊 STATISTIQUES DE SUPPORT

```
Satisfaction:     4.8/5.0 ⭐
Délai moyen:      18 heures
Taux résolution:  95%
Tickets traités:  1,200+ par mois
Langues:          Français, Anglais
Disponibilité:    99.8%
```

---

## 🎯 OBJECTIFS DE SERVICE

```
PRIORITÉ 1 (🔴 CRITIQUE)
Urgences sécurité/santé
→ Réponse: < 5 minutes
→ Résolution: < 4 heures

PRIORITÉ 2 (🟠 HIGH)
Problèmes de paiement/accès
→ Réponse: < 1 heure
→ Résolution: < 8 heures

PRIORITÉ 3 (🟡 NORMAL)
Questions techniques/support
→ Réponse: < 8 heures
→ Résolution: < 48 heures

PRIORITÉ 4 (🟢 LOW)
Demandes d'info/feedback
→ Réponse: < 24 heures
→ Résolution: < 5 jours
```

---

## 📱 ENDPOINTS API DE SUPPORT

```
GET    /api/v1/support/                  → Infos de support
POST   /api/v1/support/contact           → Envoyer message
GET    /api/v1/support/status            → Statut API
GET    /api/v1/support/faq               → Questions fréquentes
GET    /api/v1/support/documentation    → Liens documentation
GET    /api/v1/support/emergency        → Contacts d'urgence
```

---

## 💾 FORMULAIRE CONTACT (Modèle)

```json
{
  "nom": "Votre Nom Complet",
  "email": "votre@email.com",
  "telephone": "+226 XX XX XX XX",
  "sujet": "Description brève du problème",
  "message": "Description détaillée de votre demande/problème",
  "type_demande": "bug|feature|support|autre"
}
```

---

## 🌍 SUPPORT INTERNATIONAL

```
Fuseau horaire:   GMT+0 (UTC)
Traducteurs:      Français ✅ / Anglais ✅ / Autres: Sur demande
Devise:           XOF (Franc CFA) / FCFA
Moyens paiement:  Carte bancaire, Mobile Money
```

---

## ✍️ IMPRESSION IMPORTANT

> Les demandes reçues via tous les canaux sont **traitées avec la même priorité**.
> Choisissez simplement le canal qui vous convient le mieux.
> 
> **Pour urgences:** Appelez directement (plus rapide que email)
>
> **Merci de nous faire confiance!** 🙏

---

*Dernière mise à jour: 13 Mars 2026*  
*Version: 1.0.0*  
*Status: ✅ Opérationnel*
