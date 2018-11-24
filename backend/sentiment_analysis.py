# Imports the Google Cloud client library
import os
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.dirname(os.path.abspath(__file__)) + '/cloudnlp-credentials.json'

DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = "I really like Harry Potter books and movies. The Hunger Games sucks."
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document).document_sentiment

print('Text: {}'.format(text))
print('Sentiment: Score- {}, Magnitude- {}'.format(sentiment.score, sentiment.magnitude))