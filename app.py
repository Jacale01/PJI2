from flask import Flask
from router.index import traducao_bp, troca_bp

app = Flask(__name__)
app.register_blueprint(traducao_bp)
app.register_blueprint(troca_bp)


@app.route("/", methods=["GET"])
def index():
    return {
        "message": "API de Traduções e Trocas - Endpoints disponíveis: /traducao, /troca"
        
    }, 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
