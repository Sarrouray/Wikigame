import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

def get_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête HTTP: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    main_content = soup.find('div', id='mw-content-text')

    if not main_content:
        print("Contenu principal non trouvé sur la page.")
        return []

    links = []
    for a in main_content.find_all('a', href=True):
        href = a['href']
        if is_valid_link(href):
            link_text = a.text.strip()
            link_url = 'https://fr.wikipedia.org' + href
            links.append((link_text, link_url))

    return links

def is_valid_link(href):
    if not href.startswith('/wiki/'):
        return False
    if ':' in href:
        return False
    if href.startswith('/wiki/Fichier:') or href.startswith('/wiki/Aide:') or href.startswith('/wiki/Portail:'):
        return False
    if '#mw-head' in href or '#cite_note-' in href or '#cite_ref-' in href:
        return False
    return True

def play_game(request):
    start = 'Python_(langage)'  # Replace with random Wikipedia page
    target = 'Angleterre'
    current = request.POST.get('current', start)
    tour = int(request.POST.get('tour', 1))

    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice:
            try:
                choice = int(choice)
                links = get_links(f"https://fr.wikipedia.org/wiki/{current}")
                if 1 <= choice <= len(links):
                    current = links[choice - 1][1].split('/')[-1]
                    tour += 1
                    if current == target:
                        return render(request, 'wiki.html', {'message': f"Gagné en {tour} coups!", 'start': start.replace('_', ' '), 'target': target.replace('_', ' '), 'current': current.replace('_', ' '), 'tour': tour, 'links': []})
                else:
                    raise ValueError
            except ValueError:
                return render(request, 'wiki.html', {'message': "Choix invalide. Veuillez entrer un numéro valide.", 'start': start.replace('_', ' '), 'target': target.replace('_', ' '), 'current': current.replace('_', ' '), 'tour': tour, 'links': links})

    # Si c'est la première fois que la page est chargée ou après un choix valide
    links = get_links(f"https://fr.wikipedia.org/wiki/{current}")
    if not links:
        return render(request, 'wiki.html', {'message': "Pas de liens disponibles sur cette page. Essayez une autre page.", 'start': start.replace('_', ' '), 'target': target.replace('_', ' '), 'current': current.replace('_', ' '), 'tour': tour, 'links': links})

    context = {
        'start': start.replace('_', ' '),
        'target': target.replace('_', ' '),
        'current': current.replace('_', ' '),
        'tour': tour,
        'links': links,
    }

    return render(request, 'wiki.html', context)

def wiki_game_view(request):
    if request.method == 'POST':
        return play_game(request)
    else:
        start = 'Python_(langage)'  # Replace with random Wikipedia page
        target = 'Angleterre'
        current = start
        links = get_links(f"https://fr.wikipedia.org/wiki/{current}")
        if not links:
            return render(request, 'wiki.html', {'message': "Pas de liens disponibles sur cette page. Essayez une autre page."})

        context = {
            'start': start.replace('_', ' '),
            'target': target.replace('_', ' '),
            'current': current.replace('_', ' '),
            'tour': 1,
            'links': links,
        }

        return render(request, 'wiki.html', context)
