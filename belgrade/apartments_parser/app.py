import json
import time
import pika
import logging

from typing import Iterator
from apartments_adapter import ApartmentsAdapter

adapter = ApartmentsAdapter()


def get_new_apartments() -> Iterator[list]:
    res = []

    for apartments in adapter.get_apartments():
        res.clear()
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
        yield res


def send_new_apartments(data: str):
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='rabbitmq_service',
                credentials=pika.PlainCredentials('guest', 'guest')))

            channel = connection.channel()
            channel.queue_declare(queue='new_apartments')

            channel.basic_publish(exchange='',
                                  routing_key='new_apartments',
                                  body=bytes(data, 'utf-8'))
            return
        except Exception as e:
            logging.error(e)
            time.sleep(5)

def send_new_apartments_mock(data: str):
    logging.debug('Apartments result: ' + data)


def main():
    logging.basicConfig(
        format='[%(levelname)s] %(asctime)s : %(message)s',
        level=logging.INFO)

    while True:
        try:
            for batch in get_new_apartments():
                if len(batch) == 0:
                    logging.info('No new apartments were found')
                    continue

                data = json.dumps(batch)
                send_new_apartments(data)
                logging.info('Sent new batch of ' + str(len(batch)) + ' new apartments')
        except Exception as e:
            logging.error("Exception occurred for whole parsing process: " + str(e))

        time.sleep(600)


if __name__ == '__main__':
    main()
