$(document).ready(function() {
    var socket = io();
    var player_id = $('.container').data('player-id');

    $('#draw_deck1').click(function() {
        socket.emit('draw_card', { player_id: player_id, deck: 'deck1' });
        if (player_id == 1) {
            socket.emit('increment_counter');
        }
    });

    $('#draw_deck2').click(function() {
        socket.emit('draw_card', { player_id: player_id, deck: 'deck2' });
        if (player_id == 1) {
            socket.emit('increment_counter');
        }
    });

    $('#draw_character').click(function() {
        socket.emit('draw_card', { player_id: player_id, deck: 'character' });
    });

    socket.on('update', function(data) {
        var playerData = data.players['Player ' + player_id];
        $('#character').empty();
        playerData.character.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            $('#character').append(cardElement);
        });
        $('#deck1').empty();
        playerData.deck1.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            var useButton = `<button class="use-deck1-card" data-card="${card}">Aplicar</button>`;
            var sendButtons = generateSendButtons(card, 1);
            var trashButton = `<button class="send-to-trash" data-card="${card}">Lixo</button>`;
            $('#deck1').append(cardElement + useButton + sendButtons + trashButton); // Append card, use button, send buttons, and trash button
        });
        $('#deck2').empty();
        playerData.deck2.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            var sendButtons = generateSendButtons(card, 2);
            var trashButton = `<button class="send-to-trash" data-card="${card}">Lixo</button>`;
            $('#deck2').append(cardElement + sendButtons + trashButton); // Append card, send buttons, and trash button
        });
        $('#board').empty();
        playerData.board.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            var trashButton = `<button class="send-to-trash" data-card="${card}">Lixo</button>`;
            var moveButtonToDeck1 = `<button class="move-to-deck1" data-card="${card}">--> Mão Utopia</button>`;
            var sendButtons = generateSendButtons(card, "board");
            var sendToDeck1 = `<button class="send_to_deck1" data-card="${card}">--> Monte Utopia</button>`;
            $('#board').append(cardElement + trashButton, moveButtonToDeck1, sendButtons, sendToDeck1); // Append card, trash button, move to deck 1 and sendButtons
        });

        $('#other_players_boards').empty();
        Object.keys(data.players).forEach(function(player) {
            if (player !== 'Player ' + player_id) {
                var playerBoard = `<div class="other-player-board"><h3>${player}'s Board</h3>`;
                data.players[player].board.forEach(function(card) {
                    playerBoard += `<div>${card}</div>`;
                });
                playerBoard += `</div>`;
                $('#other_players_boards').append(playerBoard);
            }
        });
    });

    $('#shuffle_player_deck1').click(function() {
        socket.emit('shuffle_player_deck', { player_id: player_id, deck: 'deck1' });
    });

    $('#shuffle_player_deck2').click(function() {
        socket.emit('shuffle_player_deck', { player_id: player_id, deck: 'deck2' });
    });

    $(document).on('click', '.use-deck1-card', function() {
        var card = $(this).data('card');
        socket.emit('use_card', { player_id: player_id, card: card });
    });

    $(document).on('click', '.send-card', function() {
        var card = $(this).data('card');
        var targetPlayer = $(this).data('target-player');
        var targetDeck = $(this).data('target-deck');
        socket.emit('send_card', { player_id: player_id, card: card, target_player: targetPlayer, target_deck: targetDeck });
    });

    $(document).on('click', '.send-to-trash', function() {
        var card = $(this).data('card');
        socket.emit('send_card_to_trash', { player_id: player_id, card: card });
    });

    $(document).on('click', '.move-to-deck1', function() {
        var card = $(this).data('card');
        socket.emit('move_to_deck1', { player_id: player_id, card: card });
    });

    $(document).on('click', '.send_to_deck1', function() {
        var card = $(this).data('card');
        socket.emit('send_to_deck1', { player_id: player_id, card: card });
    });

    function generateSendButtons(card, deckNumber) {
        var sendButtons = '';
        for (var i = 1; i <= 6; i++) {
            if (deckNumber == "board") {
                if (i !== player_id) {
                    sendButtons += `<button class="send-card" data-card="${card}" data-target-player="${i}" data-target-deck="board">--> Utopia Player ${i}</button>`;
                }
            }
            else {
                if (i !== player_id) {
                    sendButtons += `<button class="send-card" data-card="${card}" data-target-player="${i}" data-target-deck="deck${deckNumber}">--> Player ${i}</button>`;
                }
            }                    
        }
        return sendButtons;
    }
});