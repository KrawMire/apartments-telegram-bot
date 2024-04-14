import logging
from flask import Flask, jsonify
from apartments_adapter import ApartmentsAdapter

app = Flask(__name__)
adapter = ApartmentsAdapter()


@app.route('/apartments-get', methods=['GET'])
def get_apartments():
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

    logging.info('Returned ' + str(len(apartments)) + ' apartments')
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
