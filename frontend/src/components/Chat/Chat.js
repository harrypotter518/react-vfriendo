import React, {Component} from 'react'

import './Chat.css'

const API_ENDPOINT = 'http://localhost:8000/api'

class Chat extends Component {
  state = {
    messages: [
      {from: 1, contents: 'Hello!'},
      {from: 0, contents: 'Hello to you too!'},
      {from: 1, contents: 'What\'s up?'},
      {from: 1, contents: 'Hello!'},
      {from: 0, contents: 'Hello to you too!'},
      {from: 1, contents: 'What\'s up?'},
      {from: 1, contents: 'Hello!'},
      {from: 0, contents: 'Hello to you too!'},
      {from: 1, contents: 'What\'s up?'},
      {from: 1, contents: 'Hello!'},
      {from: 0, contents: 'Hello to you too!'},
      {from: 1, contents: 'What\'s up?'},
      {from: 1, contents: 'Hello!'},
      {from: 0, contents: 'Hello to you too!'},
      {from: 1, contents: 'What\'s up?'},
      {from: 1, contents: 'Hello!'},
      {from: 0, contents: 'Hello to you too!'},
      {from: 0, contents: 'Hello to you too!'},
      {from: 1, contents: 'What\'s up?'},
      {from: 1, contents: 'Hello!'},
      {from: 0, contents: 'Hello to you too!'},
      {from: 1, contents: 'What\'s up?'},
      {from: 1, contents: 'Hello!'},
      {from: 0, contents: 'Hello to you too!'},
      {from: 1, contents: 'What\'s up?'},
    ],
    message: '',
  }

  chatContent = null

  componentDidMount() {
    setTimeout(this.scrollChatDown, 0)
    setTimeout(this.scrollChatDown, 100)
  }

  groupedMessages = () => {
    const groupedMessages = []
    this.state.messages.forEach(message => {
      if (!groupedMessages.length || groupedMessages[groupedMessages.length - 1].from !== message.from) {
        groupedMessages.push({from: message.from, messages: [message]})
      } else {
        groupedMessages[groupedMessages.length - 1].messages.push(message)
      }
    })

    return groupedMessages
  }

  scrollChatDown = () => {
    const {chatContent: chat} = this

    if (chat) {
      chat.scrollTop = chat.scrollHeight - chat.clientHeight
    }
  }

  handleMessageChanged = e => {
    this.setState({
      message: e.target.value,
    })
  }

  handleSendMessage = e => {
    e.preventDefault()

    const body = JSON.stringify({
      contents: this.state.message,
    })

    fetch(`${API_ENDPOINT}/messaging/messages/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body,
    })
      .then(res => res.json())
      .then(res => {
        this.setState(
          state => ({
            messages: [...state.messages, {from: 1, contents: res.contents}],
            message: '',
          }),
          this.scrollChatDown,
        )
      })
  }

  render() {
    const {messages, message} = this.state
    console.log(this.groupedMessages())

    return (
      <div className="chat__container">
        <div className="chat__header">
          <div className="header__container">
            <div>
              <div className="header__name">Some Guy</div>
              <div className="header__status">Active now</div>
            </div>
          </div>
        </div>
        <div
          className="chat__content"
          ref={ref => {
            this.chatContent = ref
          }}
        >
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message__container ${
                message.from === 1
                  ? 'message__container--mine'
                  : 'message__container--others'
                }`}
            >
              <div className="message">{message.contents}</div>
            </div>
          ))}
        </div>
        <form className="input__container" onSubmit={this.handleSendMessage}>
          <input
            className="input__input"
            type="text"
            placeholder="Type your message..."
            name="message"
            value={message}
            onChange={this.handleMessageChanged}
          />
          <button type="submit" className="input__submit">
            <svg
              x="0px"
              y="0px"
              viewBox="0 0 448.011 448.011"
              style={{enableBackground: 'new 0 0 448.011 448.011'}}
            >
              <g>
                <path
                  d="M438.731,209.463l-416-192c-6.624-3.008-14.528-1.216-19.136,4.48c-4.64,5.696-4.8,13.792-0.384,19.648l136.8,182.4    l-136.8,182.4c-4.416,5.856-4.256,13.984,0.352,19.648c3.104,3.872,7.744,5.952,12.448,5.952c2.272,0,4.544-0.48,6.688-1.472    l416-192c5.696-2.624,9.312-8.288,9.312-14.528S444.395,212.087,438.731,209.463z"/>
              </g>
            </svg>
          </button>
        </form>
      </div>
    )
  }
}

export default Chat
