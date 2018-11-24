import os

from sentiment_analysis import SentimentAnalysis
import aiml

class chatbot():
    sentiment = SentimentAnalysis()
    knowledge = {}
    historybuffer = list() # contains the 10 most recent messages
    # The Kernel object is the public interface to
    # the AIML interpreter.
    aimlBot = aiml.Kernel()
    # Use the 'learn' method to load the contents
    # of an AIML file into the Kernel.
    aimlBot.learn(os.path.dirname(os.path.abspath(__file__)) + '/botdata/*/*.aiml')

    def __init__(self):
        x = 1 #init


    def read_input(self, input):
        self.historybuffer.insert(0, input)
        if self.historybuffer.__sizeof__() == 10:
            self.historybuffer.pop()
        self.knowledge = self.sentiment.analyse_text(self.knowledge, input)
        # TODO returns either the response or some null state which maeans no response

    def reply(self, message, case):
        if case=="aiml":
            return self.aimlresponse(message)


    # TODO  actual bot architecture


    def aimlresponse(self, input):
        return self.aimlBot.respond(input)


bot = chatbot()
print(bot.aimlresponse("I am amazing"))
print(bot.aimlresponse("What do you like to do in your free time?"))