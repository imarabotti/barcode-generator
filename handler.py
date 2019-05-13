import json
import os

import boto3

from barcode.itf import ITF, IllegalCharacterError
from barcode.writer import ImageWriter


def main(event, context):
    data = json.loads(event['body'])

    try:
        barcode = ITF(data['barcode'], writer=ImageWriter())

        barcode.save('/tmp/barcode')

        s3 = boto3.resource('s3')

        barcode_data = open('/tmp/barcode.png', 'rb')

        s3.Bucket(os.environ['bucket']).put_object(
            Key='barcodes/{0}.png'.format(data['name']),
            Body=barcode_data,
            ACL='public-read'
        )

        response_body = {
            "message": "Codigo de barras generado {0}.png".format(data['name'])
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }

        return response

    except IllegalCharacterError:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "El codigo de barras es incorrecto {0}".format(data['barcode'])
            })
        }

        return response


if __name__ == '__main__':
    response = main({'body': '{"barcode": "044726000000719061002400000002460000000000000012345678944", "name": "2"}'}, None)
    print(response)
