from backend.sentiment_analysis import SentimentAnalysis


class chatbot():
    sentiment = SentimentAnalysis()

    def __init__(self):
        x = 1 #init


    def read_input(self, input):
        entities = self.sentiment.analyse_text(input)


