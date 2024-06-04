import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random
from dotenv import load_dotenv
from helpers import import_deck


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app)

original_utopia_deck = []
original_acao_deck = []
original_characters_deck = ["Gorda", "Trabalhadora", "Ninja", "Amiga", "Blogueira", "Envergonhada"]

import_deck('data/utopia_cards.csv', original_utopia_deck, 'Utopia')
import_deck('data/acao_cards.csv', original_acao_deck, 'Ação')

characters_deck = original_characters_deck.copy()
utopia_deck = original_utopia_deck.copy()
acao_deck = original_acao_deck.copy()
utopia_trash_deck = []
acao_trash_deck = []
players = {f'Player {i}': {'utopia_hand': [], 'acao_hand': [], 'board': [], 'character_hand': []} for i in range(1, 7)}
counter = -5
previous_player = 1

decks_mapping = {
    'utopia_deck': (utopia_deck, 'utopia_hand'),
    'acao_deck': (acao_deck, 'acao_hand'),
    'characters_deck': (characters_deck, 'character_hand')
}



@app.route('/')
def index():
    return render_template('index.html', counter=counter)

@app.route('/player/<int:player_id>')
def player(player_id):
    return render_template('player.html', player_id=player_id, previous_player=previous_player)

@app.route('/trash')
def trash():
    return render_template('trash.html', utopia_trash_deck=utopia_trash_deck, acao_trash_deck=acao_trash_deck)

def broadcast_game_state():
    emit('update', {
        'utopia_deck': utopia_deck,
        'acao_deck': acao_deck,
        'characters_deck': characters_deck,
        'utopia_trash_deck': utopia_trash_deck,
        'acao_trash_deck': acao_trash_deck,
        'players': players,
        'previous_player': previous_player,
        'counter': counter
    }, broadcast=True)

@socketio.on('connect')
def handle_connect():
    broadcast_game_state()

@socketio.on('disconnect')
def handle_disconnect():
    broadcast_game_state()
    
@socketio.on('increment_counter')
def increment_counter():
    global counter
    counter += 1
    broadcast_game_state()

@socketio.on('draw_card')
def draw_card(data):
    player_id = f'Player {data["player_id"]}'
    deck_name = data['deck']
    global previous_player
    previous_player = data["player_id"]
    if deck_name in decks_mapping:
        deck, hand = decks_mapping[deck_name]
        if deck:
            card = deck.pop()
            players[player_id][hand].append(card)
    broadcast_game_state()

@socketio.on('shuffle_deck')
def shuffle_deck(data):
    deck_name = data['deck']
    if deck_name in decks_mapping:
        random.shuffle(decks_mapping[deck_name][0])
    broadcast_game_state()

@socketio.on('shuffle_player_deck')
def shuffle_player_deck(data):
    player_id = f'Player {data["player_id"]}'
    deck_name = data['deck']
    if deck_name == 'utopia_hand':
        random.shuffle(players[player_id]['utopia_hand'])
    elif deck_name == 'acao_hand':
        random.shuffle(players[player_id]['acao_hand'])
    broadcast_game_state()

@socketio.on('reset_game')
def reset_game():
    global utopia_deck, acao_deck, characters_deck, utopia_trash_deck, acao_trash_deck, players, counter, decks_mapping
    utopia_deck = original_utopia_deck.copy()
    acao_deck = original_acao_deck.copy()
    characters_deck = original_characters_deck.copy()
    utopia_trash_deck = []
    acao_trash_deck = []
    counter = -5
    players = {f'Player {i}': {'utopia_hand': [], 'acao_hand': [], 'board': [], 'character_hand': []} for i in range(1, 7)}
    decks_mapping['utopia_deck'] = (utopia_deck, 'utopia_hand')
    decks_mapping['acao_deck'] = (acao_deck, 'acao_hand')
    decks_mapping['characters_deck'] = (characters_deck, 'character_hand')
    broadcast_game_state()

@socketio.on('use_card')
def use_card(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    if card in players[player_id]['utopia_hand']:
        players[player_id]['utopia_hand'].remove(card)
    elif card in players[player_id]['acao_hand']:
        players[player_id]['acao_hand'].remove(card)
    players[player_id]['board'].append(card)
    broadcast_game_state()

@socketio.on('send_card')
def send_card(data):
    player_id = f'Player {data["player_id"]}'
    target_player = f'Player {data["target_player"]}'
    card = data['card']
    target_deck = data['target_deck']
    if card in players[player_id][target_deck]:
        players[player_id][target_deck].remove(card)
        players[target_player][target_deck].append(card)
    broadcast_game_state()

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
    broadcast_game_state()

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
    broadcast_game_state()

@socketio.on('move_to_utopia_hand')
def move_to_utopia_hand(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    players[player_id]['board'].remove(card)
    players[player_id]['utopia_hand'].append(card)
    broadcast_game_state()

@socketio.on('send_to_utopia_deck')
def send_to_utopia_deck(data):
    player_id = f'Player {data["player_id"]}'
    card = data['card']
    players[player_id]['board'].remove(card)
    utopia_deck.append(card)
    broadcast_game_state()

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
    broadcast_game_state()


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    socketio.run(app, debug=debug_mode)