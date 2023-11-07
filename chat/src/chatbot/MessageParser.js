class MessageParser {
    constructor(actionProvider) {
        this.actionProvider = actionProvider
    }

    parse(message) {
        const mensaje = message.toLowerCase()

        if (mensaje.includes('!comenzar')){
            this.actionProvider.registrarUsuario(mensaje)
        }

        if (mensaje == '!comandos'){
            this.actionProvider.comandos()
        }

        if (mensaje == '!jugadores'){
            this.actionProvider.verJugadores()
        }
    }

}

export default MessageParser