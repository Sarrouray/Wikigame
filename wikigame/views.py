from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from collections import deque
import requests
from bs4 import BeautifulSoup

# Constante pour le nombre maximal de secondes autorisées
MAX_SECONDS_ALLOWED = 300  # 5 minutes

def get_random_wikipedia_page():
    """Récupère un titre de page Wikipedia aléatoire."""
    url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": 1,
        "rnnamespace": 0
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        page = data['query']['random'][0]
        title = page['title']
        return title.replace(' ', '_')  # Remplace les espaces par des underscores pour les URLs
    except Exception as e:
        print(f"Erreur lors de la récupération de la page aléatoire : {e}")
        return "Python_(langage)"  # Valeur par défaut en cas d'erreur

def get_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête HTTP: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    main_content = soup.find('div', id='mw-content-text').find('div', class_='mw-parser-output')

    if not main_content:
        print("Contenu principal non trouvé sur la page.")
        return []

    links = []
    for a in main_content.find_all('a', href=True):
        href = a['href']
        if is_valid_link(href):
            link_text = a.text.strip()
            link_url = 'https://fr.wikipedia.org' + href
            links.append((link_text, link_url))  # Garder seulement le texte et l'URL

    return links

def is_valid_link(href):
    if not href.startswith('/wiki/'):
        return False
    if ':' in href:
        return False
    if href.startswith('/wiki/Fichier:') or href.startswith('/wiki/Aide:') or href.startswith('/wiki/Portail:'):
        return False
    if '#mw-head' in href or '#cite_note-' in href or '#cite_ref-' in href or '#toc' in href:
        return False
    return True

def get_wikipedia_summary(title):
    base_url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": title
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        summary = page['extract']
        return summary
    except Exception as e:
        print(f"Erreur lors de la récupération du résumé Wikipedia : {e}")
        return None

def shortest_path(start, target):
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        current, path = queue.popleft()

        if current == target:
            return path

        for link_text, link_url in get_links(f"https://fr.wikipedia.org/wiki/{current}"):
            next_page = link_url.split('/')[-1]
            if next_page not in visited:
                visited.add(next_page)
                queue.append((next_page, path + [next_page]))

    return None

def simulate_game(start, target):
    """Simule une partie gagnée entre deux pages Wikipedia."""
    path = shortest_path(start, target)
    if path:
        return {
            'message': f"Gagné en {len(path) - 1} coups !",
            'history': path,
            'elapsed_minutes': 0,
            'elapsed_seconds': 0
        }
    else:
        return {
            'message': "Impossible de trouver un chemin.",
            'history': [],
            'elapsed_minutes': 0,
            'elapsed_seconds': 0
        }

def wiki_game_view(request):
    # Initialiser la variable show_shortest_path
    show_shortest_path = False

    if request.method == 'POST':
        if 'show_replay' in request.POST:
            # Réinitialiser le jeu
            request.session.pop('start_time', None)
            request.session.pop('current', None)
            request.session.pop('tour', None)
            request.session.pop('history', None)
            return redirect('wiki_game_view')
        
        elif 'simulate' in request.POST:
            # Simuler le jeu
            simulate = request.POST.get('simulate') == 'true'
            if simulate:
                start = "Python_(langage)"  # Page de départ fixe pour la simulation
                target = "Pays-Bas"  # Page cible fixe pour la simulation
                simulation_result = simulate_game(start, target)
                return render(request, 'wiki.html', {
                    'message': simulation_result['message'],
                    'start': start.replace('_', ' '),
                    'target': target.replace('_', ' '),
                    'current': start.replace('_', ' '),
                    'tour': 1,
                    'links': [],
                    'page': 1,
                    'total_pages': 1,
                    'elapsed_minutes': simulation_result['elapsed_minutes'],
                    'elapsed_seconds': simulation_result['elapsed_seconds'],
                    'history': simulation_result['history'],
                    'shortest_path': shortest_path(start, target),
                    'show_shortest_path': show_shortest_path
                })
        
        elif 'show_shortest_path' in request.POST:
            # Afficher le chemin le plus court
            show_shortest_path = True
        
        else:
            choice = request.POST.get('choice')
            if choice is not None:
                try:
                    choice = int(choice)
                    current = request.POST.get('current')
                    tour = int(request.POST.get('tour'))
                    page = int(request.POST.get('page'))

                    links = get_links(f"https://fr.wikipedia.org/wiki/{current}")

                    if 0 <= choice < len(links):
                        current = links[choice][1].split('/')[-1]  # Utilisation de l'URL (index 1)
                        tour += 1
                        if current == request.session.get('target'):
                            # Calcul du temps écoulé
                            end_time = datetime.now()
                            start_time_iso = request.session.get('start_time')
                            start_time = datetime.fromisoformat(start_time_iso)
                            elapsed_time = end_time - start_time
                            if elapsed_time > timedelta(seconds=MAX_SECONDS_ALLOWED):
                                return render(request, 'wiki.html', {
                                    'message': "Temps écoulé ! Vous avez perdu.",
                                    'start': request.session.get('start').replace('_', ' '),
                                    'target': request.session.get('target').replace('_', ' '),
                                    'current': current.replace('_', ' '),
                                    'tour': tour,
                                    'links': [],
                                    'page': page,
                                    'total_pages': 1,
                                    'elapsed_minutes': int(elapsed_time.total_seconds() // 60),
                                    'elapsed_seconds': int(elapsed_time.total_seconds() % 60),
                                    'history': request.session.get('history', []),
                                    'shortest_path': shortest_path(request.session.get('start'), request.session.get('target')),
                                    'show_shortest_path': show_shortest_path,
                                })
                        request.session['current'] = current
                        request.session['tour'] = tour
                        return redirect('wiki_game_view')

                except (ValueError, IndexError):
                    pass

    # Initialisation du jeu
    if 'start' not in request.session or 'target' not in request.session:
        start = get_random_wikipedia_page()
        target = get_random_wikipedia_page()
        request.session['start'] = start
        request.session['target'] = target
        request.session['current'] = start
        request.session['tour'] = 1
        request.session['start_time'] = datetime.now().isoformat()
        request.session['history'] = []

    start = request.session['start']
    target = request.session['target']
    current = request.session.get('current', start)
    tour = request.session.get('tour', 1)
    page = int(request.POST.get('page', 1))

    links = get_links(f"https://fr.wikipedia.org/wiki/{current}")

    per_page = 20
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_links = links[start_index:end_index]
    total_pages = (len(links) + per_page - 1) // per_page

    paginated_links_with_index = list(enumerate(paginated_links, start=start_index))

    elapsed_time = datetime.now() - datetime.fromisoformat(request.session.get('start_time'))
    elapsed_minutes = int(elapsed_time.total_seconds() // 60)
    elapsed_seconds = int(elapsed_time.total_seconds() % 60)

    context = {
        'start': start.replace('_', ' '),
        'target': target.replace('_', ' '),
        'current': current.replace('_', ' '),
        'tour': tour,
        'links': paginated_links_with_index,
        'page': page,
        'total_pages': total_pages,
        'elapsed_minutes': elapsed_minutes,
        'elapsed_seconds': elapsed_seconds,
        'history': request.session.get('history', []),
        'shortest_path': shortest_path(start, target) if show_shortest_path else None,
        'show_shortest_path': show_shortest_path,
    }

    return render(request, 'wiki.html', context)
