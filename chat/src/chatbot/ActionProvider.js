import use from 'react'
import { typescript } from '../../next.config'
import { execOnce } from 'next/dist/shared/lib/utils'

class ActionProvider {
    mensajeError = "Hubo un problema con la conexión de la Granja... Vuelvelo a intentar en unos segundos"
    
    endpoint = "http://localhost:5001"

    constructor(createChatBotMessage, setStateFunc) {
        this.createChatBotMessage = createChatBotMessage
        this.setState = setStateFunc
    }

    updateChatbotState(message) {
           this.setState(prevState => ({
                ...prevState, messages: [...prevState.messages, message]
            }))
          }

    comandos () {
        const mensaje = this.createChatBotMessage(`Actualmente estos son los comandos disponibles:
                                                   !comenzar Nombre username contraseña para crear tu usuario
                                                   !jugadores para ver los jugadores que hay actualmente`)
        this.updateChatbotState(mensaje)
    }

    comenzar (){
        const mensaje = this.createChatBotMessage(`Para comenzar escribe tu nombre y tu contraseña
        Ejemplo: usuario,contraseña`)
        this.updateChatbotState(mensaje)
    }

    async verJugadores(){
        try{
            const response = await fetch(this.endpoint, {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    query: '{listUsers{name, id}}',
                })
            })

            const data = await response.json()
            if(data.errors) {
                throw new Error(data.errors[0].message)
            }

            let mensaje = data.data.listUsers
            if (mensaje == undefined) {
                mensaje = []
            }
            console.log(mensaje)

            const respuesta = this.createChatBotMessage(`Aqui estan los jugadores actuales:`,{widget:"userList", payload:{mensaje}})
            this.updateChatbotState(respuesta)


        } catch (error) {
            this.createChatBotMessage(this.mensajeError)
            this.updateChatbotState(this.mensajeError)
            }
        }
    async registrarUsuario(mensaje){
        try{
            const temp = mensaje.split(' ')
            const len = temp.length
            if (len < 3){
                const respuesta = this.createChatBotMessage(`Faltan datos para registrarte!!!
                                                             Recuerda que es Nombre username contraseña
                                                             Sin comas de por medio`)
                this.updateChatbotState(respuesta)
            }

            const respuesta= await fetch(this.endpoint,{
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    query: `mutation {
                        createUser(name: "${temp[1]}", username: "${temp[2]}", password: "${temp[3]}") {
                          name
                        }
                      }`,
                })
            })
            
            const data = await respuesta.json()
            if (data === null){
                const resp = this.createChatBotMessage("Hubo un problema al crear tu usuario, prueba en unos segundos más...")
                this.updateChatbotState(resp)
            }

            const resp = this.createChatBotMessage(`Bienvenido ${data.data.createUser.name} recuerda utilizar !comandos para ver los comandos disponibles`)
            this.updateChatbotState(resp)

    

        }catch{
        
        }
    }
}

export default ActionProvider