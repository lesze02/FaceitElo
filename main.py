import json

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def wczytaj_klucz():
    with open('C:/Users/Lesze/PycharmProjects/KluczFaceit.txt') as plik:
        for linia in plik:
            return linia

API_KEY = wczytaj_klucz()


def pobierz_id_gracza(nick):
    url = f'https://open.faceit.com/data/v4/players?nickname={nick}'
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['player_id']
    else:
        return False


def pobierz_staty(player_id):
    url = f'https://open.faceit.com/data/v4/players/{player_id}/stats/cs2'
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f'Error: {response.status_code}\n{response.text}'


def pobierz_staty_10(player_id):
    url = f'https://open.faceit.com/data/v4/players/{player_id}/games/cs2/stats'
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    params = {
        'offset': 0,
        'limit': 10
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        staty = response.json()

        kille = licz_staty('Kills', staty, 'int')
        aststy = licz_staty('Assists', staty, 'int')
        deaths = licz_staty('Deaths', staty, 'int')
        kdr = round(licz_staty('K/D Ratio', staty, 'float'),2)
        krr = round(licz_staty('K/R Ratio', staty, 'float'), 2)
        hs = licz_staty('Headshots %', staty, 'int')

        print(kdr)
        return staty

    else:
        return f'Error: {response.status_code}\n{response.text}'


def licz_staty(nazwa_statystyki, staty, wersja):
    if (wersja == 'int'):
        tablica = [int(item['stats'][nazwa_statystyki]) for item in staty['items']]
    elif (wersja == 'float'):
        tablica = [float(item['stats'][nazwa_statystyki]) for item in staty['items']]
    wartosc = sum(tablica) / len(tablica)
    return wartosc


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/stats', methods=['GET'])
def stats():
    nick = request.args.get('nick')
    if (nick):
        player_id = pobierz_id_gracza(nick)
        if (player_id):
            staty = pobierz_staty(player_id)
            if (staty):
                statystyki_calosciowe = {
                    'Matches': staty['lifetime']['Matches'],
                    'HS': staty['lifetime']['Average Headshots %'],
                    'KDR': staty['lifetime']['Average K/D Ratio'],
                    'Wins': staty['lifetime']['Wins'],
                    'ADR': staty['lifetime']['ADR'],
                    'WR ': staty['lifetime']['Win Rate %'],
                    'ostatnie_wyniki ': staty['lifetime']['Recent Results']
                }
    return render_template('stats.html', nick=nick, statystyki_calosciowe=statystyki_calosciowe)


if __name__ == "__main__":
    player_id = pobierz_id_gracza('RO0js')
    stats = pobierz_staty_10(player_id)
    print(json.dumps(stats, indent=4))
    # print(stats)

    # app.run(debug=True)
