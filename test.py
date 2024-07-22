import requests
from bs4 import BeautifulSoup
import sys

def get_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête HTTP: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = [
        (a.text.strip(), 'https://fr.wikipedia.org' + a['href'])
        for a in soup.find_all('a', href=True)
        if a['href'].startswith('/wiki/') and ':' not in a['href']
    ]
    
    if not links:
        print("Aucun lien trouvé sur la page.")
    else:
        print(f"{len(links)} liens trouvés.")
    
    return links

def play_game(start, target):
    current = start
    tour = 1
    while current != target:
        print(f"\n************************ WikiGame **** tour {tour}")
        print(f"Départ : {start.replace('_', ' ')}")
        print(f"Cible : {target.replace('_', ' ')}")
        print(f"Actuellement : {current.replace('_', ' ')}\n")
        
        links = get_links(f"https://fr.wikipedia.org/wiki/{current}")
        if not links:
            print("Pas de liens disponibles sur cette page. Essayez une autre page.")
            return
        
        total_links = len(links)
        page = 0
        
        while current != target:
            start_index = page * 20
            end_index = start_index + 20
            display_links = links[start_index:end_index]
            
            for i, (text, url) in enumerate(display_links, start=1):
                print(f"{i:02d} - {text}")
            
            if start_index > 0:
                print("98 - Page précédente")
            if end_index < total_links:
                print("99 - Voir la suite")
            
            try:
                choice = int(input("Votre choix : "))
                if choice == 98 and start_index > 0:
                    page -= 1
                    continue
                elif choice == 99 and end_index < total_links:
                    page += 1
                    continue
                elif 1 <= choice <= len(display_links):
                    current = display_links[choice - 1][1].split('/')[-1]
                    tour += 1
                    page = 0  # Reset to the first page of links for the new page
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Choix invalide. Veuillez entrer un numéro valide.")
    
    print(f"Gagné en {tour - 1} coups!")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Il faut 2 paramètres ou plus")
        exit(1)
    start, target = sys.argv[1], sys.argv[2]
    play_game(start, target)
