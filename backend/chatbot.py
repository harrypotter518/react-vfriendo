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

    def read_input(self, input):
        self.historybuffer.insert(0, input)
        if self.historybuffer.__sizeof__() == 10:
            self.historybuffer.pop()
        self.knowledge = self.sentiment.analyse_text(self.knowledge, input)
        if(input.contains("@bot") or input.contains("@Bot")):
            return self.reply(input, "location")
        return self.reply(input, "aiml")

    def reply(self, message, case):
        if case=="aiml":
            return self.aimlresponse(message)
        elif case=="location":
            return "Location time"

    def aimlresponse(self, input):
        return self.aimlBot.respond(input)


    # Returns the top 3 interests of the person
    def returnInterests(self):
        topthree = list()
        for entity in self.knowledge.values():
            if entity.isPositive() is False:
                continue
            if topthree.__sizeof__() < 3:
                topthree.append(entity)
            elif topthree[2].overallSent() < entity.overallSent():
                topthree.insert(0, entity)
                topthree.pop()
        return topthree


