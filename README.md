# Bitcoin Notifier

Notification sonore dès que le prix du Bitcoin bouge — à la hausse comme à la baisse.

Une petite application de bureau qui interroge l'API publique CoinGecko toutes les
15 secondes et joue un son différent selon la direction du mouvement.

## Fonctionnalités

- Cours du Bitcoin en euros, récupéré via l'API publique CoinGecko
- Surveillance en arrière-plan dans un thread dédié
- Effets sonores distincts pour la hausse et la baisse
- Fenêtre de statut qui affiche le cours et la variation
- Sons et icône personnalisables (fichiers `.wav` et `.ico` à la racine)

## Stack

- **Python** — `requests` pour l'API, `customtkinter` pour l'interface
- **CoinGecko API** — endpoint public, aucune clé requise

## Démarrage

```bash
pip install requests customtkinter
python main.py
```

Les réglages (délai de polling, URL de l'API, police) sont dans `settings.py`.

## Fichiers

| Fichier | Rôle |
| :--- | :--- |
| `main.py` | Point d'entrée : polling, thread de surveillance, lecture des sons |
| `settings.py` | Configuration : intervalle, URL d'API, polices |
| `*.wav` | Effets sonores (synthé 80s, bris de verre, variation) |
| `Blank.ico` | Icône de l'application |

## Licence

Usage personnel. Les fichiers audio inclus sont utilisés à titre illustratif.
