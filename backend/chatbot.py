import os

from sentiment_analysis import SentimentAnalysis
import aiml
import os

from google.cloud import language


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
        self.historybuffer.insert(0, input)
        if self.historybuffer.__sizeof__() == 10:
            self.historybuffer.pop()
        self.knowledge = self.sentiment.analyse_text(self.knowledge, input)
        if "@bot" or "@Bot" in input:
            return self.reply(input, "location")
        return self.reply(input, "aiml")

    def reply(self, message, case):
        if case == "aiml":
            return {
                'message': self.aimlresponse(message),
            }
        elif case == "location":
            group = self.classify(self.historytext())
            return {
                'message': "Location time",
            }

    def aimlresponse(self, input):
        return self.aimlBot.respond(input)

    def historytext(self):
        text = ""
        for t in self.historybuffer[::-1]:
            text += t + "\n"
        return text

    def classify(self, text):
        """Classify the input text into categories. """

        language_client = language.LanguageServiceClient()

        document = language.types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)
        response = language_client.classify_text(document)
        categories = response.categories, verbose=True

        result = list()

        for category in categories:
            # Turn the categories into a dictionary of the form:
            # {category.name: category.confidence}, so that they can
            # be treated as a sparse vector.
            if category.confidence < 0.1:
                continue
            result.append(category)
        return result

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



