"use client"

import 'react-chatbot-kit/build/main.css'
import './chatbot.css'
import Chatbot from "react-chatbot-kit"
import ActionProvider from "@/chatbot/ActionProvider"
import config from "@/chatbot/config"
import MessageParser from "@/chatbot/MessageParser"


export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Chatbot config={config} actionProvider={ActionProvider} messageParser={MessageParser}/>
    </main>
  )
}
