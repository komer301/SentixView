from flask import Flask, request
from flask_restful import Api, Resource
import sentiment
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class SentimentAnalysis(Resource):
    def get(self, videoID):
        try:
            result = sentiment.analysis(videoID)
            return result, 200
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return {"error": str(e)}, 500

api.add_resource(SentimentAnalysis, "/<string:videoID>")
if __name__ == "__main__":
    app.run(debug=True)