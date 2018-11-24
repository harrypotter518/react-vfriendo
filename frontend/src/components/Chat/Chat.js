import React, { Component } from 'react'

import './Chat.css'

class Chat extends Component {
  state = {
    messages: [
      { from: 1, contents: 'Hello!' },
      { from: 0, contents: 'Hello to you too!' },
      { from: 1, contents: "What's up?" },
      { from: 1, contents: 'Hello!' },
      { from: 0, contents: 'Hello to you too!' },
      { from: 1, contents: "What's up?" },
      { from: 1, contents: 'Hello!' },
      { from: 0, contents: 'Hello to you too!' },
      { from: 1, contents: "What's up?" },
      { from: 1, contents: 'Hello!' },
      { from: 0, contents: 'Hello to you too!' },
      { from: 1, contents: "What's up?" },
      { from: 1, contents: 'Hello!' },
      { from: 0, contents: 'Hello to you too!' },
      { from: 1, contents: "What's up?" },
      { from: 1, contents: 'Hello!' },
      { from: 0, contents: 'Hello to you too!' },
      { from: 0, contents: 'Hello to you too!' },
      { from: 1, contents: "What's up?" },
      { from: 1, contents: 'Hello!' },
      { from: 0, contents: 'Hello to you too!' },
      { from: 1, contents: "What's up?" },
      { from: 1, contents: 'Hello!' },
      { from: 0, contents: 'Hello to you too!' },
      { from: 1, contents: "What's up?" },
    ],
    message: '',
  }

  chatContent = null

  componentDidMount() {
    setTimeout(this.scrollChatDown, 0)
    setTimeout(this.scrollChatDown, 100)
  }

  scrollChatDown = () => {
    const { chatContent: chat } = this

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
    this.setState(
      state => ({
        messages: [...state.messages, { from: 1, contents: state.message }],
        message: '',
      }),
      this.scrollChatDown,
    )
  }

  render() {
    const { messages, message } = this.state

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
            <svg viewBox="0 0 18 16" version="1.1" xmlns="http://www.w3.org/2000/svg">
                <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <g id="Screen-1" transform="translate(-323.000000, -615.000000)" fill="#027CF7">
                        <g id="Textarea" transform="translate(12.000000, 591.000000)">
                            <g id="send-btn" transform="translate(299.000000, 8.000000)">
                                <g id="icon" transform="translate(12.000000, 10.000000)">
                                    <path d="M18.6685794,10.731995 L3.81179211,4.0502042 C3.57522634,3.94552281 3.29294738,4.00788619 3.12837989,4.20611265 C2.96266957,4.40433911 2.95695542,4.68608795 3.11466594,4.88988257 L8.00026328,11.2375838 L3.11466594,17.585285 C2.95695542,17.7890797 2.96266957,18.0719421 3.12723706,18.269055 C3.23809155,18.4038044 3.40380187,18.4761905 3.57179785,18.4761905 C3.65293877,18.4761905 3.73407968,18.459486 3.81064928,18.4249634 L18.6674365,11.7431726 C18.8708602,11.6518548 19,11.454742 19,11.2375838 C19,11.0204256 18.8708602,10.8233128 18.6685794,10.731995 Z" id="Path" transform="translate(11.000000, 11.238095) rotate(-33.000000) translate(-11.000000, -11.238095) "></path>
                                </g>
                            </g>
                        </g>
                    </g>
                </g>
            </svg>
          </button>
        </form>
      </div>
    )
  }
}

export default Chat
