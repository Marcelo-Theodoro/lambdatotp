import botocore
import boto3
from boto3.dynamodb.conditions import Key

from pyotp import random_base32

from chalicelib.util import log

from chalicelib.config import REGION, TABLE_NAME


class TOTPBase:

    def __init__(self, region, table_name):
        self.database = boto3.resource('dynamodb', region_name=region)
        self.table = self.database.Table(table_name)

    def get_user(self, user_id):
        item = self.table.get_item(Key={'user_id': user_id})

        try:
            return item['Item']
        except KeyError:
            raise ValueError('User not found')


    def save_new_user(self, user_id, secret=random_base32()):
        try:
            self.table.put_item(
                Item={
                    'user_id': user_id,
                    'secret': secret,
                },
                ConditionExpression='attribute_not_exists(user_id)'
            )
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ValueError('User already in the database')
            else:
                log('models.save_new_user',
                    f'Error while trying to save a new user: {err.response}')
                raise err
        return {'user_id': user_id, 'secret': secret}


    def delete_user(self, user_id):
        try:
            self.table.delete_item(
                Key={
                    'user_id': user_id,
                },
                ConditionExpression='attribute_exists(user_id)'
            )
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ValueError('User not found in the database')
            else:
                log('models.delete_user',
                    f'Error while trying to delete a user: {err.response}')
                raise err
        return True

DATABASE = TOTPBase(REGION, TABLE_NAME)
