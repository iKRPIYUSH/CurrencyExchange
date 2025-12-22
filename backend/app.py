from flask import Flask, request, jsonify
import json

app = Flask(__name__)

with open("exchange_rates.json", "r") as f:
    EXCHANGE_RATES = json.load(f)


def get_rate(from_currency, to_currency):
    return EXCHANGE_RATES.get(f"{from_currency}_{to_currency}")


@app.route("/convert", methods=["GET"])
def convert_currency():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    amount = float(request.args.get("amount"))

    rate = get_rate(from_currency, to_currency)
    if rate is None:
        return jsonify({"error": "Rate not found"}), 404

    return jsonify({
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "rate": rate,
        "convertedAmount": round(amount * rate, 2)
    })


@app.route("/rate", methods=["GET"])
def exchange_rate():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")

    rate = get_rate(from_currency, to_currency)
    if rate is None:
        return jsonify({"error": "Rate not found"}), 404

    return jsonify({
        "from": from_currency,
        "to": to_currency,
        "rate": rate
    })


if __name__ == "__main__":
    app.run(debug=True)
