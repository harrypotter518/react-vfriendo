# Imports the Google Cloud client library
import statistics as stat
import os
import sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.dirname(os.path.abspath(__file__)) + '/cloudapi-credentials.json'

DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')


class SentimentAnalysis:
    """A class for handling sentiment analysis of text."""

    def __init__(self):
        self.client = language.LanguageServiceClient()
        # Detect and send native Python encoding to receive correct word offsets.
        self.encoding = enums.EncodingType.UTF32
        if sys.maxunicode == 65535:
            self.encoding = enums.EncodingType.UTF16

    def analyse_text(self, knowledge, text):
        existingEntities = knowledge
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)
        sentiment = self.client.analyze_entity_sentiment(document=document, encoding_type=self.encoding)
        for entity in sentiment.entities:
            if entity.name in existingEntities.keys():
                idea = existingEntities.get(entity.name)
            else:
                idea = (SentimentEntity(entity.name, entity.type))
            sentimentlist = list()
            magnitudelist = list()
            for mention in entity.mentions:
                s = mention.sentiment.score
                if s is None: s = 0
                m = mention.sentiment.magnitude
                if m is None: m = 0
                sentimentlist.append(s)
                magnitudelist.append(m)
                idea.addSentiments(sentimentlist, magnitudelist)
                existingEntities[idea.name] = idea
        return existingEntities


class SentimentEntity:
    """A class for storing sentimence information."""
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.score = list()
        self.scoreVal = 0
        self.magnitude = list()
        self.magVal = 0
        self.nummentions = 0

    def addSentiments(self, scorelist, magnitudelist):
        self.score.extend(scorelist)
        self.scoreVal = stat.mean(self.score)
        self.magnitude.extend(magnitudelist)
        self.magVal = stat.mean(self.magnitude)
        self.nummentions = self.nummentions + scorelist.__sizeof__()

    def sentimence(self):
        val = self.magVal*self.scoreVal
        if val > 0.8:
            return 1 # positive
        elif val < -0.4:
            return -1 # negative
        else:
            return 0 # neutral

    def overallsent(self):
        return self.magVal*self.scoreVal

    def isPositive(self):
        if self.overallsent() > 0.8: # current thresholds subject to change
            return True
        else:
            return False

    def isNegative(self):
        if self.overallsent() < -0.4: # current thresholds subject to change
            return True
        else:
            return False

    def isNeutral(self):
        if self.overallsent() > -0.4 and self.overallsent() < 0.8: # current thresholds subject to change
            return True
        else:
            return False