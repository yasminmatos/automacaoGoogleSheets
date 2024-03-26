from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/posts')
def get_posts():
    # Dados fictícios de posts
    marketing_data = [
        {
            "id": 1,
            "campanha": "Campanha de Verão",
            "tipo": "Pesquisa",
            "custo": 2500.50,
            "cliques": 1200,
            "conversoes": 30
        },
        {
            "id": 2,
            "campanha": "Campanha de Outono",
            "tipo": "Display",
            "custo": 1800.75,
            "cliques": 900,
            "conversoes": 20
        },
        {
            "id": 3,
            "campanha": "Campanha de Inverno",
            "tipo": "Vídeo",
            "custo": 3200.25,
            "cliques": 1500,
            "conversoes": 40
        },
        {
            "id": 4,
            "campanha": "Campanha de Primavera",
            "tipo": "Pesquisa",
            "custo": 2800.60,
            "cliques": 1100,
            "conversoes": 35
        },
        {
            "id": 5,
            "campanha": "Campanha de Natal",
            "tipo": "Display",
            "custo": 4000.00,
            "cliques": 2000,
            "conversoes": 50
        }
    ]
    return jsonify(marketing_data)

if __name__ == '__main__':
    app.run(port=5000)
