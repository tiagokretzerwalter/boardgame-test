$(document).ready(function() {
    var socket = io();

    $('#reset_utopia_trash_deck').click(function() {
        socket.emit('reset_trash', { deck: 'utopia_trash_deck' });
    });

    $('#reset_acao_trash_deck').click(function() {
        socket.emit('reset_trash', { deck: 'acao_trash_deck' });
    });
    
    socket.on('update', function(data) {
        $('#utopia_trash_deck').empty();
        data.utopia_trash_deck.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            var sendButtons = generateSendButtons(card);
            $('#utopia_trash_deck').append(cardElement + sendButtons);
        });
        $('#acao_trash_deck').empty();
        data.acao_trash_deck.forEach(function(card) {
            var cardElement = `<div>${card}</div>`;
            var sendButtons = generateSendButtons(card);
            $('#acao_trash_deck').append(cardElement + sendButtons);
        });
    });

    $(document).on('click', '.send-from-trash', function() {
        var card = $(this).data('card');
        var targetPlayer = $(this).data('target-player');
        socket.emit('send_card_from_trash', { target_player: targetPlayer, card: card });
    });

    function generateSendButtons(card) {
        var sendButtons = '';
        for (var i = 1; i <= 6; i++) {
            sendButtons += `<button class="send-from-trash" data-card="${card}" data-target-player="${i}" >--> Player ${i}</button>`;
            
        }
        return sendButtons;
    }
});