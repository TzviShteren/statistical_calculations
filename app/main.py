from app.routs.questions_a_rout import questions_a_blueprint
from app.routs.heatmap_rout import heatmap_blueprint
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app)

load_dotenv(verbose=True)

app.register_blueprint(questions_a_blueprint, url_prefix="/api/questions_a")
app.register_blueprint(heatmap_blueprint, url_prefix="/api/heatmap")

if __name__ == '__main__':
    app.run()
