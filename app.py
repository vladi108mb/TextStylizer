from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Cargar modelo de spaCy en español
nlp = spacy.load("es_core_news_sm")

# Reglas de estilo
style_rules = {
    "ADJ": {"color": "#32CD32"},
    "VERB": {"color": "#FF00FF"},
    "NOUN": {"color": "#00BFFF"},
    "ADV": {"color": "#0000FF"},
    # Agrega más reglas aquí si lo necesitas
}

@app.route('/procesar', methods=['POST'])
def procesar_texto():
    datos = request.json
    texto = datos.get("texto", "")

    if not texto:
        return jsonify({"error": "No se proporcionó texto para procesar."}), 400

    doc_spacy = nlp(texto)
    resultado = []

    for token in doc_spacy:
        estilo = style_rules.get(token.pos_, {"color": "#000000"})
        resultado.append({"text": token.text, "color": estilo["color"]})

    return jsonify({"tokens": resultado})

if __name__ == "__main__":
    app.run(debug=True)
