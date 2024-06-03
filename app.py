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

original_utopia_deck = []
original_acao_deck = []

with open(utopia_csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        original_utopia_deck.append(row['Utopia'])

with open(acao_csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        original_acao_deck.append(row['Ação'])

original_characters_deck = ["Gorda", "Trabalhadora", "Ninja", "Amiga", "Blogueira", "Envergonhada"]
characters_deck = original_characters_deck.copy()
utopia_deck = original_utopia_deck.copy()
acao_deck = original_acao_deck.copy()
utopia_trash_deck = []
acao_trash_deck = []
players = {f'Player {i}': {'utopia_hand': [], 'acao_hand': [], 'board': [], 'character': []} for i in range(1, 7)}
counter = -5
previous_player = 1



@app.route('/')
def index():
    return render_template('index.html', counter=counter)

@app.route('/player/<int:player_id>')
def player(player_id):
    return render_template('player.html', player_id=player_id, previous_player=previous_player)

@app.route('/trash')
def trash():
    return render_template('trash.html', utopia_trash_deck=utopia_trash_deck, acao_trash_deck=acao_trash_deck)

@socketio.on('connect')
def handle_connect():
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)
    emit('update_counter', {'counter': counter})

@socketio.on('disconnect')
def handle_disconnect():
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)
    
@socketio.on('increment_counter')
def increment_counter():
    global counter
    counter += 1
    emit('update_counter', {'counter': counter}, broadcast=True)

@socketio.on('draw_card')
def draw_card(data):
    player_id = f'Player {data["player_id"]}'
    deck_name = data['deck']
    global previous_player
    previous_player = data["player_id"]
    if deck_name == 'utopia_deck' and utopia_deck:
        card = utopia_deck.pop()
        players[player_id]['utopia_hand'].append(card)
    elif deck_name == 'acao_deck' and acao_deck:
        card = acao_deck.pop()
        players[player_id]['acao_hand'].append(card)
    elif deck_name == 'character' and characters_deck:
        card = characters_deck.pop()
        players[player_id]['character'].append(card)    
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('shuffle_deck')
def shuffle_deck(data):
    deck_name = data['deck']
    if deck_name == 'utopia_deck':
        random.shuffle(utopia_deck)
    elif deck_name == 'acao_deck':
        random.shuffle(acao_deck)
    elif deck_name == "characters_deck":
        random.shuffle(characters_deck)
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('shuffle_player_deck')
def shuffle_player_deck(data):
    player_id = f'Player {data["player_id"]}'
    deck_name = data['deck']
    if deck_name == 'utopia_hand':
        random.shuffle(players[player_id]['utopia_hand'])
    elif deck_name == 'acao_hand':
        random.shuffle(players[player_id]['acao_hand'])
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('reset_game')
def reset_game():
    global utopia_deck, utopia_deck, utopia_trash_deck, acao_trash_deck, players
    utopia_deck = original_utopia_deck.copy()
    acao_deck = original_acao_deck.copy()
    characters_deck = original_characters_deck.copy()
    utopia_trash_deck = []
    acao_trash_deck = []
    players = {f'Player {i}': {'utopia_hand': [], 'acao_hand': [], 'board': [], 'character': []} for i in range(1, 7)}
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('use_card')
def use_card(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    if card in players[player_id]['utopia_hand']:
        players[player_id]['utopia_hand'].remove(card)
    elif card in players[player_id]['acao_hand']:
        players[player_id]['acao_hand'].remove(card)
    players[player_id]['board'].append(card)
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('send_card')
def send_card(data):
    player_id = f'Player {data["player_id"]}'
    target_player = f'Player {data["target_player"]}'
    card = data['card']
    target_deck = data['target_deck']
    if card in players[player_id][target_deck]:
        players[player_id][target_deck].remove(card)
        players[target_player][target_deck].append(card)
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('send_card_to_trash')
def send_card_to_trash(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    if card in players[player_id]['utopia_hand']:
        players[player_id]['utopia_hand'].remove(card)
        utopia_trash_deck.append(card)
    elif card in players[player_id]['acao_hand']:
        players[player_id]['acao_hand'].remove(card)
        acao_trash_deck.append(card)
    elif card in players[player_id]['board']:
        players[player_id]['board'].remove(card)
        utopia_trash_deck.append(card)    
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('send_card_from_trash')
def send_card_from_trash(data):
    target_player = f'Player {data["target_player"]}'
    card = data['card']
    if card in acao_trash_deck:
        acao_trash_deck.remove(card)
        players[target_player]['acao_hand'].append(card)
    if card in utopia_trash_deck:
        utopia_trash_deck.remove(card)
        players[target_player]['utopia_hand'].append(card)
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('move_to_utopia_hand')
def move_to_utopia_hand(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    players[player_id]['board'].remove(card)
    players[player_id]['utopia_hand'].append(card)
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('send_to_utopia_deck')
def send_to_utopia_deck(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    players[player_id]['board'].remove(card)
    utopia_deck.append(card)
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)

@socketio.on('reset_trash')
def reset_trash(data):
    global utopia_trash_deck, acao_trash_deck
    deck_name = data['deck']
    if deck_name == 'utopia_trash_deck':
        utopia_deck.extend(utopia_trash_deck)
        utopia_trash_deck = []
    if deck_name == 'acao_trash_deck':
        acao_deck.extend(acao_trash_deck)
        acao_trash_deck = []    
    emit('update', {'utopia_deck': utopia_deck, 'acao_deck': acao_deck, 'characters_deck': characters_deck, 'utopia_trash_deck': utopia_trash_deck, 'acao_trash_deck': acao_trash_deck, 'players': players, 'previous_player': previous_player}, broadcast=True)


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    socketio.run(app, debug=debug_mode)