import React, {Component} from 'react'

import './Chat.css'

const API_ENDPOINT = 'http://localhost:8000/api'

const OTHER_RESPONSES = [
  {from: 0, contents: 'Sup?'},
  null,
  {from: 0, contents: 'nothing much, have any plans for tonight?'},
  {from: 0, contents: 'Yeah I could go for a pizza or smth'},
  null,
  {from: 0, contents: 'What kind of pizza would you like?'},
  {from: 0, contents: 'Yeah, that was delicious, do we have any pizzerias here that server that?'},
  {from: 0, contents: 'ask your bot friend'},
]

class Chat extends Component {
  state = {
    messages: [
      OTHER_RESPONSES[0],
      // {from: 2, options: ['Dinner', 'Entertainment', 'Shopping'], selected: "Entertainment"}
    ],
    message: '',
    isSubmitting: false,
    currentOtherIndex: 1,
  }

  chatContent = null

  componentDidMount() {
    setTimeout(this.scrollChatDown, 0)
    setTimeout(this.scrollChatDown, 100)
  }

  whoSaidIt = (from) => {
     if (from === 1) {
         return 'message__container--mine'
     } else if (from === 2) {
         return 'message__container--others message__container--bot'
     } else {
         return 'message__container--others'
     }
  }

  groupedMessages = () => {
    const groupedMessages = []
    this.state.messages.forEach((message, index) => {
        const newMessage = {...message, index}
        if (message.options) {
            groupedMessages.push({from: message.from, messages: [newMessage], option: true})

        } else if (!groupedMessages.length || groupedMessages[groupedMessages.length - 1].from !== message.from) {
        groupedMessages.push({from: message.from, messages: [newMessage]})
      } else {
        groupedMessages[groupedMessages.length - 1].messages.push(newMessage)
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

  handleOptionSelected = (message, option) => {
      this.setState({
          messages: [
              ...this.state.messages.slice(0, message.index),
              {...this.state.messages[message.index], selected: option},
              ...this.state.messages.slice(message.index + 1)
          ]
      })
  }

  handleSendMessage = e => {
    e.preventDefault()

    if (!this.state.message || this.state.isSubmitting) {
      return
    }

    const { message } = this.state

    this.setState(
      state => ({
        messages: [...state.messages, {from: 1, contents: message}],
        message: '',
        isSubmitting: true,
      }),
      this.scrollChatDown,
    )

    navigator.geolocation.getCurrentPosition(position => {
      const { latitude, longitude } = position.coords

      const body = JSON.stringify({
        contents: message,
        user_id: 1,
        longitude,
        latitude,
      })

      fetch(`${API_ENDPOINT}/messaging/messages/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body,
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
            state => {
              const newMessages = [...state.messages]

              if (res.bot_response) {
                newMessages.push({
                  from: 2,
                  contents: res.bot_response.message,
                })

                if (res.bot_response.options) {
                  newMessages.push({
                    from: 2,
                    options: res.bot_response.options,
                    selected: null,
                  })
                }
              }

              return {
                messages: newMessages,
                isSubmitting: false,
              }
            },
            this.scrollChatDown,
          )

          setTimeout(() => {
            const index = this.state.currentOtherIndex

            this.setState({
              currentOtherIndex: index + 1,
            })

            this.setState(state => {
              if (OTHER_RESPONSES.length < index) {
                return {}
              }

              const message = OTHER_RESPONSES[index]

              if (!message) {
                return {}
              }

              fetch(`${API_ENDPOINT}/messaging/messages/`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  contents: message.contents,
                  user_id: 1,
                  longitude,
                  latitude,
                }),
              })

              return {
                messages: [...state.messages, message],
              }
            }, this.scrollChatDown)
          }, 1000)
        })
        .catch(err => {
          console.error(err)
          this.setState({
            isSubmitting: false,
          })
        })
    })
  }

  render() {
    const {message, isSubmitting} = this.state

    return (
      <div className="chat__container">
        <div className="chat__header">
          <div className="header__container">
            <a href="#" className="back-btn">
                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 129 129" enableBackground="new 0 0 129 129">
                  <g>
                    <path d="m88.6,121.3c0.8,0.8 1.8,1.2 2.9,1.2s2.1-0.4 2.9-1.2c1.6-1.6 1.6-4.2 0-5.8l-51-51 51-51c1.6-1.6 1.6-4.2 0-5.8s-4.2-1.6-5.8,0l-54,53.9c-1.6,1.6-1.6,4.2 0,5.8l54,53.9z"/>
                  </g>
                </svg>
            </a>
            <div>
              <div className="header__name">Malcolm Function</div>
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
          {this.groupedMessages().map((group, index) => (
            <div
              key={index}
              className={`message__container ${this.whoSaidIt(group.from)}`}
            >
                {group.from !== 1 && !group.option && (
                    <div className={`avatar ${
                        (group.from === 2 ? 'bot': '')
                    }`}></div>
                )}
                <div className="message__container--inner">
                    {group.messages.map((message, index_1) => {
                        if (!message.contents && message.options) {
                            return (
                                <div
                                    key={index_1}
                                    className="option__container">
                                    {message.options.map(option => {
                                        return (
                                            <button
                                                key={option}
                                                className={`option ${
                                                    message.selected === option ? "selected" : ""}`}
                                                onClick={() => this.handleOptionSelected(message,option)}
                                                >{option}
                                            </button>
                                        )
                                    }) }
                                </div>
                            )
                        } else {
                            return (
                                <div
                                    key={index_1}
                                    className="message">{message.contents}
                                </div>
                            )
                        }
                    })}
                </div>
            </div>
          ))}

        </div>
        <form className="input__container" onSubmit={this.handleSendMessage}>
          <input
            className="input__input"
            type="text"
            placeholder="Type your message..."
            name="message"
            autoComplete="off"
            value={message}
            onChange={this.handleMessageChanged}
          />
          <button type="submit" className="input__submit" disabled={isSubmitting}>
            <svg viewBox="0 0 18 16" version="1.1" xmlns="http://www.w3.org/2000/svg">
                <g id="Page-1" stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
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
