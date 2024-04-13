from flask import Flask, jsonify

from apartments_adapter import ApartmentsAdapter

app = Flask(__name__)


@app.route('/apartments-get', methods=['GET'])
def get_apartments():
    adapter = ApartmentsAdapter()
    apartments = adapter.get_apartments()
    res = []

    for apartment in apartments:
        res.append({
            'title': apartment.title,
            'description': apartment.description,
            'link': apartment.link,
            'placement': apartment.placement,
            'price': apartment.price,
            'owner': apartment.owner,
            'date_published': apartment.date_published,
            'features': apartment.features
        })

    return jsonify(res)


if __name__ == '__main__':
    app.run()
