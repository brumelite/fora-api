# Fortune Rabbit (Fora)

Une API REST gratuite et open source proposant des phrases aléatoires, des réponses et une phrase du jour commune à tous les utilisateurs.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green)

## API publique

**URL :** https://api.fora.brumelite.com

**Documentation Swagger :** https://api.fora.brumelite.com/docs

## Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/health` | État du service |
| GET | `/v1/fortunes/random` | Phrase aléatoire |
| GET | `/v1/fortunes/daily` | Phrase du jour |
| GET | `/v1/fortunes/answer` | Réponse aléatoire |
| GET | `/v1/fortunes/{id}` | Phrase par identifiant |
| GET | `/v1/categories` | Catégories disponibles |
| GET | `/v1/languages` | Langues disponibles |

## Hébergement et déploiement

![Vercel](https://img.shields.io/badge/Vercel-000000?logo=vercel&logoColor=white)
![Neon](https://img.shields.io/badge/Neon-00E599?logo=neon&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

- **Vercel** — Hébergement de l'API FastAPI.
- **Neon** — Base de données PostgreSQL.
- **GitHub Actions** — Tests automatisés et déploiement continu.

## Licence

Distribué sous licence **MIT**. Voir [LICENSE](LICENSE).