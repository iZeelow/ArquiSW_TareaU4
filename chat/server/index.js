const http = require('http');

const server = http.createServer();

port = 3000

const io = require('socket.io')(server, {
    cors: { origin: '*' }
});

io.on('connection', (socket) => {
    console.log("Se ha conectado un cliente");

    socket.on('chat_message', (data) => {
        io.emit('chat_message', data);
    })

});

server.listen(port);
