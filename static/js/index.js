$(document).ready(function() {
    var socket = io();

    $('#shuffle_deck1').click(function() {
        socket.emit('shuffle_deck', { deck: 'deck1' });
    });

    $('#shuffle_deck2').click(function() {
        socket.emit('shuffle_deck', { deck: 'deck2' });
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