$(document).ready(function() {
    var socket = io();
    var player_id = $('.container').data('player-id');

    attachEventHandlers();

    socket.on('update', function(data) {
        var playerData = data.players['Player ' + player_id];
        updateHand('#character_hand', playerData.character_hand, 'character');
        updateHand('#utopia_hand', playerData.utopia_hand, 'utopia');
        updateHand('#acao_hand', playerData.acao_hand, 'acao');
        updateHand('#board', playerData.board, 'board');
        updateOtherPlayersBoards('#other_players_boards', data.players);
        $('#previous_player').text(data.previous_player);
    });

    function attachEventHandlers() {
        $('#draw_utopia_card').click(function() {
            drawCard('utopia_deck');
        });

        $('#draw_acao_card').click(function() {
            drawCard('acao_deck');
        });

        $('#draw_character').click(function() {
            drawCard('characters_deck');
        });

        $('#shuffle_player_utopia_hand').click(function() {
            shuffleDeck('utopia_hand');
        });
    
        $('#shuffle_player_acao_hand').click(function() {
            shuffleDeck('acao_hand');
        });
    
        $(document).on('click', '.use-utopia-card', function() {
            var cardId = $(this).data('card-id');
            socket.emit('use_card', { player_id: player_id, card_id: cardId });
        });
    
        $(document).on('click', '.send-card', function() {
            var cardId = $(this).data('card-id');
            var targetPlayer = $(this).data('target-player');
            var targetDeck = $(this).data('target-deck');
            socket.emit('send_card_to_player', { player_id: player_id, card_id: cardId, target_player: targetPlayer, target_deck: targetDeck });
        });
    
        $(document).on('click', '.send-to-trash', function() {
            var cardId = $(this).data('card-id');
            socket.emit('send_card_to_trash', { player_id: player_id, card_id: cardId });
        });
    
        $(document).on('click', '.move-to-utopia-hand', function() {
            var cardId = $(this).data('card-id');
            socket.emit('move_to_utopia', { player_id: player_id, card_id: cardId, target_deck: "utopia_hand" });
        });
    
        $(document).on('click', '.send_to_utopia_deck', function() {
            var cardId = $(this).data('card-id');
            socket.emit('move_to_utopia', { player_id: player_id, card_id: cardId, target_deck: "utopia_deck" });
        });
    };    

    function updateHand(elementId, handData, handType) {
        var element = $(elementId);
        element.empty();
        handData.forEach(function(card) {
            var cardElement = `<div>${card.name}</div>`;
            var useButton = handType === 'utopia' ? `<button class="use-utopia-card" data-card-id="${card.id}">Aplicar</button>` : '';
            var sendButtons = (handType === 'utopia' || handType === 'acao' || handType === 'board') ? generateSendButtons(card, handType) : '';
            var trashButton = (handType === 'utopia' || handType === 'acao' || handType === 'board') ? `<button class="send-to-trash" data-card-id="${card.id}">Lixo</button>` : '';
            var moveButtonToUtopiaHand = (handType === 'board') ? `<button class="move-to-utopia-hand" data-card-id="${card.id}">--> Mão Utopia</button>` : '';
            var sendToUtopiaDeck = (handType === 'utopia' || handType === 'board') ? `<button class="send_to_utopia_deck" data-card-id="${card.id}">--> Monte Utopia</button>` : '';
            element.append(cardElement + useButton + sendButtons + trashButton + moveButtonToUtopiaHand + sendToUtopiaDeck);
        });
    };

    function updateOtherPlayersBoards(elementId, playersData) {
        var element = $(elementId);
        element.empty();
        Object.keys(playersData).forEach(function(player) {
            if (player !== 'Player ' + player_id) {
                var playerBoard = `<div class="other-player-board"><h3>${player}'s Board</h3>`;
                var cardNumber = 1;
                playersData[player].board.forEach(function(card) {
                    playerBoard += `<div>${cardNumber} - ${card.name}</div>`;
                    cardNumber += 1;
                });
                playerBoard += `</div>`;
                element.append(playerBoard);
            }
        });
    };

    function drawCard(deck) {
        socket.emit('draw_card', { player_id: player_id, deck: deck });
        if (player_id == 1 && deck != 'characters_deck') {
            socket.emit('increment_counter');
        };
    };

    function shuffleDeck(deck) {
        socket.emit('shuffle_deck', { player_id: player_id, deck: deck });
    };

    function generateSendButtons(card, deckName) {
        var sendButtons = '';
        for (var i = 1; i <= 6; i++) {
            if (deckName == "board") {
                if (i !== player_id) {
                    sendButtons += `<button class="send-card" data-card-id="${card.id}" data-target-player="${i}" data-target-deck="board">--> Utopia Player ${i}</button>`;
                };
            }
            else {
                if (i !== player_id) {
                    sendButtons += `<button class="send-card" data-card-id="${card.id}" data-target-player="${i}" data-target-deck="${deckName}_hand">--> Player ${i}</button>`;
                };
            };              
        };
        return sendButtons;
    };
});