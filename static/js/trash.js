$(document).ready(function() {
    var socket = io();

    attachEventHandlers();

    socket.on('update', function(data) {
        updateTrashDeck('utopia_trash_deck', data.utopia_trash_deck);
        updateTrashDeck('acao_trash_deck', data.acao_trash_deck);
    });

    function attachEventHandlers() {
        $('#reset_utopia_trash_deck').click(function() {
            socket.emit('reset_trash', { deck: 'utopia_trash_deck' });
        });

        $('#reset_acao_trash_deck').click(function() {
            socket.emit('reset_trash', { deck: 'acao_trash_deck' });
        });

        $(document).on('click', '.send-from-trash', function() {
            var cardId = $(this).data('card-id');
            var targetPlayer = $(this).data('target-player');
            socket.emit('send_card_from_trash', { target_player: targetPlayer, card_id: cardId });
        });
    };
    
    function updateTrashDeck(deckId, deckData) {
        var deckElement = $('#' + deckId);
        deckElement.empty();
        deckData.forEach(function(card) {
            var cardElement = `<div>${card.name}</div>`;
            var sendButtons = generateSendButtons(card);
            deckElement.append(cardElement + sendButtons);
        });
    }

    function generateSendButtons(card) {
        var sendButtons = '';
        for (var i = 1; i <= 6; i++) {
            sendButtons += `<button class="send-from-trash" data-card-id="${card.id}" data-target-player="${i}" >--> Player ${i}</button>`;
            
        };
        return sendButtons;
    };
});