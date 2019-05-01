import json
import os

import boto3

from barcode.itf import ITF
from barcode.writer import ImageWriter


def main(event, context):
    data = json.loads(event['body'])

    barcode = ITF(data['barcode'], writer=ImageWriter())

    barcode.save('/tmp/barcode')

    s3 = boto3.resource('s3')

    barcode_data = open('/tmp/barcode.png', 'rb')

    s3.Bucket(os.environ['bucket']).put_object(Key='barcodes/{0}.png'.format(data['name']), Body=barcode_data)

    response_body = {
        "message": "Codigo de barras generado {0}.png".format(data['name'])
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }

    return response


if __name__ == '__main__':
    main({'Records': [{'body': '{"barcode": "12312311123312441233"}'}]}, None)
