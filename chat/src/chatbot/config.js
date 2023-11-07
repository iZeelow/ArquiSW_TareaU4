import { createChatBotMessage } from 'react-chatbot-kit';

import Avatar from './Avatar';

import UserList from './widgets/userList';

const config = { 
  botName: "Chatbot Granja",
  widgets: [
    {
        widgetName: 'userList',
        widgetFunc: (props) => <UserList {... props}/>
    }
    ],
  initialMessages: [createChatBotMessage(`Hola, gracias por usar el Chatbot Granja V1.0
                                          Escribe !comandos para ver los comandos disponibles o
                                          !comenzar nombre username contraseña para registrarte!`)],
  customComponents: { 
    botAvatar: (props) => <Avatar {... props}/>,
    header: () => <div className='react-chatbot-kit-chat-header'>Conversando Con Chatbot Granja V1.0</div>,
    
  },
  
}

export default config