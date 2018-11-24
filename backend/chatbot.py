from sentiment_analysis import SentimentAnalysis
import aiml

class chatbot():
    sentiment = SentimentAnalysis()
    knowledge = list()

    def __init__(self):
        x = 1 #init


    def read_input(self, input):
        self.knowledge.append
        self.sentiment.analyse_text(input)
        # TODO returns either the response or some null state which maeans no response


    def reply(self):
        return "This is a response"

    # TODO  actual bot architecture


    def aimlresponse(self):

        # The Kernel object is the public interface to
        # the AIML interpreter.
        k = aiml.Kernel()

        # Use the 'learn' method to load the contents
        # of an AIML file into the Kernel.
        k.learn("std-startup.xml")

        # Use the 'respond' method to compute the response
        # to a user's input string.  respond() returns
        # the interpreter's response, which in this case
        # we ignore.
        k.respond("What is botname")

        # Loop forever, reading user input from the command
        # line and printing responses.
        print(k.respond("fish"))


bot = chatbot()
bot.aimlresponse()