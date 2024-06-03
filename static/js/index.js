$(document).ready(function() {
    var socket = io();

    $('#shuffle_utopia_deck').click(function() {
        socket.emit('shuffle_deck', { deck: 'utopia_deck' });
    });

    $('#shuffle_acao_deck').click(function() {
        socket.emit('shuffle_deck', { deck: 'acao_deck' });
    });

    $('#shuffle_characters').click(function() {
        socket.emit('shuffle_deck', { deck: 'characters_deck' });
    });

    $('#reset_game').click(function() {
        socket.emit('reset_game');
    });

    socket.on('update_counter', function(data) {
        $('#draw-counter').text(data.counter);
    });
});