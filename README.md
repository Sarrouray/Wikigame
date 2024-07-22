# WikiGame

WikiGame est un jeu éducatif qui consiste à trouver le chemin le plus court entre deux pages Wikipedia en naviguant uniquement via les liens hypertextes disponibles sur les pages.

## Fonctionnalités

- Obtenez une page Wikipedia de départ et une page d'arrivée aléatoires.
- Cliquez sur les liens des pages pour vous rapprocher de la page cible.
- Simulez une partie pour voir le chemin le plus court entre deux pages spécifiques.
- Affichez le chemin le plus court si vous êtes bloqué.

## Prérequis

- Python 3.x
- Django
- requests
- BeautifulSoup4

## Installation

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/Sarrouray/Wikigame.git
    cd Wikigame
    ```

2. Créez et activez un environnement virtuel :
    ```sh
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances :
    ```sh
    pip install -r requirements.txt
    ```

4. Lancez le serveur de développement :
    ```sh
    python manage.py runserver 8000
    ```

5. Ouvrez votre navigateur et accédez à `http://127.0.0.1:8000/wikigame` pour jouer au jeu.

## Utilisation

1. **Nouvelle Partie** : En accédant à la page principale, une nouvelle partie est automatiquement démarrée avec une page de départ et une page cible aléatoires.
2. **Navigation** : Cliquez sur les liens des pages Wikipedia pour vous rapprocher de la page cible.
3. **Simulation** : Utilisez le formulaire pour simuler une partie avec des pages spécifiques de départ et d'arrivée.
4. **Afficher le Chemin le Plus Court** : Cliquez sur le bouton pour afficher le chemin le plus court si vous êtes bloqué.

## Structure du Projet

- `manage.py`: Script principal pour interagir avec le projet Django.
- `myapp/`: Répertoire de l'application principale contenant les vues, modèles, et autres composants.
  - `views.py`: Contient la logique des vues pour le jeu.
  - `urls.py`: Définit les routes URL pour l'application.
  - `templates/`: Contient les fichiers HTML pour le rendu des pages.
- `static/`: Contient les fichiers statiques comme les CSS et JavaScript.
- `requirements.txt`: Liste des dépendances Python pour le projet.

## Contribution

1. Forkez le projet.
2. Créez une nouvelle branche (`git checkout -b feature/ma-nouvelle-fonctionnalité`).
3. Commitez vos modifications (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`).
4. Poussez votre branche (`git push origin feature/ma-nouvelle-fonctionnalité`).
5. Créez une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.


