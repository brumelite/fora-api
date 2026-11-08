# Fortune Rabbit (Fora)

Une API REST gratuite et open source qui propose des phrases aléatoires, des réponses et une phrase du jour commune à tous les utilisateurs.

Développée avec **Python, FastAPI et PostgreSQL**.

## Endpoints

| Méthode | Route | Description |
| --- | --- | --- |
| GET | `/health` | État du service |
| GET | `/v1/fortunes/random` | Phrase aléatoire |
| GET | `/v1/fortunes/daily` | Phrase du jour |
| GET | `/v1/fortunes/answer` | Réponse aléatoire |
| GET | `/v1/fortunes/{id}` | Phrase par identifiant |
| GET | `/v1/categories` | Catégories disponibles |
| GET | `/v1/languages` | Langues disponibles |

*Documentation et URL publiques à venir.*
