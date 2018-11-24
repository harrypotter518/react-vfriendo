import os

from sentiment_analysis import SentimentAnalysis
import aiml


class ChatBot:
    sentiment = SentimentAnalysis()
    knowledge = {}
    historybuffer = list()  # contains the 10 most recent messages
    # The Kernel object is the public interface to
    # the AIML interpreter.
    aimlBot = aiml.Kernel()
    # Use the 'learn' method to load the contents
    # of an AIML file into the Kernel.
    aimlBot.learn(os.path.dirname(os.path.abspath(__file__)) + '/botdata/*/*.aiml')

    def read_input(self, input, latitude, longitude):
        pprint(input)
        self.historybuffer.insert(0, input)
        if self.historybuffer.__sizeof__() == 10:
            self.historybuffer.pop()
        self.knowledge = self.sentiment.analyse_text(self.knowledge, input)
        if input.contains("@bot") or input.contains("@Bot"):
            return self.reply(input, "location")
        return self.reply(input, "aiml")

    def reply(self, message, case):
        if case == "aiml":
            return {
                'message': self.aimlresponse(message),
            }
        elif case == "location":
            return {
                'message': "Location time",
            }

    def aimlresponse(self, input):
        return self.aimlBot.respond(input)


bot = ChatBot()
