$(document).ready(function() {
    var socket = io();
    var player_id = $('.container').data('player-id');

    $('#draw_utopia_card').click(function() {
        socket.emit('draw_card', { player_id: player_id, deck: 'utopia_deck' });
        if (player_id == 1) {
            socket.emit('increment_counter');
        }
    });

    $('#draw_acao_card').click(function() {
        socket.emit('draw_card', { player_id: player_id, deck: 'acao_deck' });
        if (player_id == 1) {
            socket.emit('increment_counter');
        }
    });

    $('#draw_character').click(function() {
        socket.emit('draw_card', { player_id: player_id, deck: 'characters_deck' });
    });

    socket.on('update', function(data) {
        var playerData = data.players['Player ' + player_id];
        $('#character_hand').empty();
        playerData.character_hand.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            $('#character_hand').append(cardElement);
        });
        $('#utopia_hand').empty();
        playerData.utopia_hand.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            var useButton = `<button class="use-utopia-card" data-card="${card}">Aplicar</button>`;
            var sendButtons = generateSendButtons(card, "utopia");
            var trashButton = `<button class="send-to-trash" data-card="${card}">Lixo</button>`;
            $('#utopia_hand').append(cardElement + useButton + sendButtons + trashButton); // Append card, use button, send buttons, and trash button
        });
        $('#acao_hand').empty();
        playerData.acao_hand.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            var sendButtons = generateSendButtons(card, "acao");
            var trashButton = `<button class="send-to-trash" data-card="${card}">Lixo</button>`;
            $('#acao_hand').append(cardElement + sendButtons + trashButton); // Append card, send buttons, and trash button
        });
        $('#board').empty();
        playerData.board.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            var trashButton = `<button class="send-to-trash" data-card="${card}">Lixo</button>`;
            var moveButtonToUtopiaHand = `<button class="move-to-utopia-hand" data-card="${card}">--> Mão Utopia</button>`;
            var sendButtons = generateSendButtons(card, "board");
            var sendToUtopiaDeck = `<button class="send_to_utopia_deck" data-card="${card}">--> Monte Utopia</button>`;
            $('#board').append(cardElement + trashButton, moveButtonToUtopiaHand, sendButtons, sendToUtopiaDeck); // Append card, trash button, move to deck 1 and sendButtons
        });

        $('#other_players_boards').empty();
        Object.keys(data.players).forEach(function(player) {
            if (player !== 'Player ' + player_id) {
                var playerBoard = `<div class="other-player-board"><h3>${player}'s Board</h3>`;
                var cardNumber = 1
                data.players[player].board.forEach(function(card) {
                    playerBoard += `<div>${cardNumber} - ${card}</div>`;
                    cardNumber += 1;
                });
                playerBoard += `</div>`;
                $('#other_players_boards').append(playerBoard);
            }
        });
        $('#previous_player').text(data.previous_player);
    });

    $('#shuffle_player_utopia_hand').click(function() {
        socket.emit('shuffle_deck', { player_id: player_id, deck: 'utopia_hand' });
    });

    $('#shuffle_player_acao_hand').click(function() {
        socket.emit('shuffle_deck', { player_id: player_id, deck: 'acao_hand' });
    });

    $(document).on('click', '.use-utopia-card', function() {
        var card = $(this).data('card');
        socket.emit('use_card', { player_id: player_id, card: card });
    });

    $(document).on('click', '.send-card', function() {
        var card = $(this).data('card');
        var targetPlayer = $(this).data('target-player');
        var targetDeck = $(this).data('target-deck');
        socket.emit('send_card_to_player', { player_id: player_id, card: card, target_player: targetPlayer, target_deck: targetDeck });
    });

    $(document).on('click', '.send-to-trash', function() {
        var card = $(this).data('card');
        socket.emit('send_card_to_trash', { player_id: player_id, card: card });
    });

    $(document).on('click', '.move-to-utopia-hand', function() {
        var card = $(this).data('card');
        socket.emit('move_to_utopia', { player_id: player_id, card: card, target_deck: "utopia_hand" });
    });

    $(document).on('click', '.send_to_utopia_deck', function() {
        var card = $(this).data('card');
        socket.emit('move_to_utopia', { player_id: player_id, card: card, target_deck: "utopia_deck" });
    });

    function generateSendButtons(card, deckName) {
        var sendButtons = '';
        for (var i = 1; i <= 6; i++) {
            if (deckName == "board") {
                if (i !== player_id) {
                    sendButtons += `<button class="send-card" data-card="${card}" data-target-player="${i}" data-target-deck="board">--> Utopia Player ${i}</button>`;
                }
            }
            else {
                if (i !== player_id) {
                    sendButtons += `<button class="send-card" data-card="${card}" data-target-player="${i}" data-target-deck="${deckName}_hand">--> Player ${i}</button>`;
                }
            }                    
        }
        return sendButtons;
    }
});