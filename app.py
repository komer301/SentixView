from flask import Flask, request
from flask_restful import Api, Resource
import sentiment

app = Flask(__name__)
api = Api(app)

class SentimentAnalysis(Resource):
    def get(self,videoID):
        return sentiment.analysis(videoID)

api.add_resource(SentimentAnalysis, "/<string:videoID>")
if __name__ == "__main__":
    app.run(debug=True)