import boto3
from botocore.exceptions import ClientError
import os

class SNSService:
    def __init__(self):
        self.client = boto3.client(
            'sns',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'eu-east-1')
        )


    def send_sms(self, phone_number: str, message: str) -> bool:
        """
        Send SMS using AWS SNS
        :param phone_number: Phone number in E.164 format (+1234567890)
        :param message: Message content
        :return: True if successful, False otherwise
        """
        try:
            response = self.client.publish(
                PhoneNumber=phone_number,
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
            print(f"Message sent! Message ID: {response['MessageId']}")
            return True
        except ClientError as e:
            print(f"Error sending SMS: {e}")
            return False