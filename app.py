import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random
from dotenv import load_dotenv
import csv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app)

utopia_csv_file_path = 'data/utopia_cards.csv'
acao_csv_file_path = 'data/acao_cards.csv'

original_deck1 = []
original_deck2 = []

with open(utopia_csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        original_deck1.append(row['Utopia'])

with open(acao_csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        original_deck2.append(row['Ação'])

original_characters_deck = ["Gorda", "Trabalhadora", "Ninja", "Amiga", "Blogueira", "Envergonhada"]
characters_deck = original_characters_deck.copy()
deck1 = original_deck1.copy()
deck2 = original_deck2.copy()
utopia_trash_deck = []
acao_trash_deck = []
players = {f'Player {i}': {'deck1': [], 'deck2': [], 'board': [], 'character': []} for i in range(1, 7)}



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player/<int:player_id>')
def player(player_id):
    return render_template(f'player{player_id}.html', player_id=player_id)

@app.route('/trash')
def trash():
    return render_template('trash.html', utopia_trash_deck=utopia_trash_deck, acao_trash_deck=acao_trash_deck)

@socketio.on('connect')
def handle_connect():
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('draw_card')
def draw_card(data):
    player_id = f'Player {data["player_id"]}'
    deck_name = data['deck']
    if deck_name == 'deck1' and deck1:
        card = deck1.pop()
        players[player_id]['deck1'].append(card)
    elif deck_name == 'deck2' and deck2:
        card = deck2.pop()
        players[player_id]['deck2'].append(card)
    elif deck_name == 'character' and characters_deck:
        card = characters_deck.pop()
        players[player_id]['character'].append(card)
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('shuffle_deck')
def shuffle_deck(data):
    deck_name = data['deck']
    if deck_name == 'deck1':
        random.shuffle(deck1)
    elif deck_name == 'deck2':
        random.shuffle(deck2)
    elif deck_name == "characters_deck":
        random.shuffle(characters_deck)
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('shuffle_player_deck')
def shuffle_player_deck(data):
    player_id = f'Player {data["player_id"]}'
    deck_name = data['deck']
    if deck_name == 'deck1':
        random.shuffle(players[player_id]['deck1'])
    elif deck_name == 'deck2':
        random.shuffle(players[player_id]['deck2'])
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('reset_game')
def reset_game():
    global deck1, deck2, utopia_trash_deck, acao_trash_deck, players
    deck1 = original_deck1.copy()
    deck2 = original_deck2.copy()
    characters_deck = original_characters_deck.copy()
    utopia_trash_deck = []
    acao_trash_deck = []
    players = {f'Player {i}': {'deck1': [], 'deck2': [], 'board': [], 'character': []} for i in range(1, 7)}
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('use_card')
def use_card(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    if card in players[player_id]['deck1']:
        players[player_id]['deck1'].remove(card)
    elif card in players[player_id]['deck2']:
        players[player_id]['deck2'].remove(card)
    players[player_id]['board'].append(card)
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('send_card')
def send_card(data):
    player_id = f'Player {data["player_id"]}'
    target_player = f'Player {data["target_player"]}'
    card = data['card']
    target_deck = data['target_deck']
    if card in players[player_id][target_deck]:
        players[player_id][target_deck].remove(card)
        players[target_player][target_deck].append(card)
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('send_card_to_trash')
def send_card_to_trash(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    if card in players[player_id]['deck1']:
        players[player_id]['deck1'].remove(card)
        utopia_trash_deck.append(card)
    elif card in players[player_id]['deck2']:
        players[player_id]['deck2'].remove(card)
        acao_trash_deck.append(card)
    elif card in players[player_id]['board']:
        players[player_id]['board'].remove(card)
        utopia_trash_deck.append(card)    
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('send_card_from_trash')
def send_card_from_trash(data):
    target_player = f'Player {data["target_player"]}'
    card = data['card']
    if card in acao_trash_deck:
        acao_trash_deck.remove(card)
        players[target_player]['deck2'].append(card)
    if card in utopia_trash_deck:
        utopia_trash_deck.remove(card)
        players[target_player]['deck1'].append(card)
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('move_to_deck1')
def move_to_deck1(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    players[player_id]['board'].remove(card)
    players[player_id]['deck1'].append(card)
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)

@socketio.on('send_to_deck1')
def send_to_deck1(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    players[player_id]['board'].remove(card)
    deck1.append(card)
    emit('update', {'deck1': deck1, 'deck2': deck2, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players}, broadcast=True)



if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    socketio.run(app, debug=debug_mode)