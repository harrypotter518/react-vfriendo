import os

from sentiment_analysis import SentimentAnalysis
import aiml
import os
from services.google_places import search_places, PlaceType

from google.cloud import language


class ChatBot:
    sentiment = SentimentAnalysis()
    #sentiment.makemodel()
    knowledge = {}
    historybuffer = list()  # contains the 10 most recent messages
    # The Kernel object is the public interface to
    # the AIML interpreter.
    aimlBot = aiml.Kernel()
    # Use the 'learn' method to load the contents
    # of an AIML file into the Kernel.
    aimlBot.learn(os.path.dirname(os.path.abspath(__file__)) + '/botdata/*/*.aiml')
    status = False

    def read_input(self, input, latitude, longitude):
        input = input.lower()
        self.historybuffer.insert(0, input)
        if self.historybuffer.__sizeof__() == 100:
            self.historybuffer.pop()
        self.knowledge = self.sentiment.analyse_text(self.knowledge, input)
        if "@bot" in input or "@Bot" in input:
            input_list = input.split(' ')
            keyword = 'on' if len(input_list) == 1 else input_list[1]

            if keyword == 'off':
                self.status = False
            elif keyword == 'topic':
                return self.reply(input, 'topic', latitude, longitude)
            else:
                self.status = True
                return self.reply(input, "location", latitude, longitude)
        if self.status is True:
            return self.reply(input, "aiml", latitude, longitude)
        return None

    def reply(self, message, case, latitude, longitude):
        if case == "aiml":
            # group = self.classify(self.historytext())
            return {
                'message': self.aimlresponse(message),
            }
        elif case == "location":
            if len(self.historytext().split()) < 20:
                return {
                    'message': 'I am not sure about where you should go. Try talking more.',
                }

            group = self.classify(self.historytext())

            if len(group) == 0:
                return {
                    'message': 'I am not sure about where you should go. Try talking more.',
                }

            best_match = group[0]
            place_type = None
            query = ''
            if 'Restaurants' in best_match.name:
                place_type = PlaceType.restaurant
                category_split = best_match.name.strip('/').split('/')
                if len(category_split) > 2:
                    query = category_split[2]  # Fast Food or Pizzeria

            results = search_places(latitude, longitude, place_type=place_type, keyword=query)
            results = results[:4]

            return {
                'message': 'How about one of these?',
                'options': [place['name'] for place in results],
            }
        elif case == 'topic':
            interests = self.returnInterests()
            return {
                'message': 'How about one of these topics?',
                'options': [{
                    'label': interest.name,
                    'link': f'https://www.google.com/maps/dir/?api=1&destination={interest.geometry.location.lat},{interest.geometry.location.lat}',
                } for interest in interests],
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
        categories = response.categories

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
        entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                       'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
        topthree = list()
        for entity in self.knowledge.values():
            if entity.isNegative():
                continue
            elif len(topthree) < 3:
                topthree.append(entity)
            elif len(topthree) > 1 and topthree[2].overallsent() < entity.overallsent():
                topthree.insert(0, entity)
                topthree.pop()
        return topthree


bot = ChatBot()
