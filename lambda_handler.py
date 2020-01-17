# Copyright (c) 2020 Manuel Burki
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import  parse_qs


def lambda_handler(event, context):

    elements = parse_qs(event['body'])
    
    # Technical variables for SES email
    SENDER_EMAIL    = os.environ['SENDER_EMAIL']
    RECIPIENT       = os.environ['RECIPIENT']
    EMAIL_SUBJECT   = os.environ['EMAIL_SUBJECT']
    SITE_URL        = os.environ['SITE_URL']
    CHARSET         = "utf-8"
    AWS_REGION      = os.environ['AWS_REGION']

    # Form data / use POST method and Lambda proxy integration
    FORM_NAME       = elements['cf-name'][0]
    FORM_EMAIL      = elements['cf-email'][0]
    FORM_SUBJECT    = elements['cf-subject'][0]
    FORM_MESSAGE    = 'Name: ' + FORM_NAME + '\r\n' + 'Email: ' + FORM_EMAIL + '\r\n' + \
                      'Subject: ' + FORM_SUBJECT + '\r\n' + \
                      'Message: ' + '\n\n' + elements['cf-message'][0]

    client = boto3.client('ses',region_name=AWS_REGION)

    msg = MIMEMultipart('mixed')
    msg['Subject'] = EMAIL_SUBJECT 
    msg['From'] = SENDER_EMAIL 
    msg['To'] = RECIPIENT

    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(FORM_MESSAGE.encode(CHARSET), 'plain', CHARSET)
    msg_body.attach(textpart)
    msg.attach(msg_body)

    try:
        response = client.send_raw_email(
            Source=SENDER_EMAIL,
            Destinations=[ RECIPIENT ],
            RawMessage={ 'Data':msg.as_string(), }
        )

    except ClientError as e:
        resp_msg = '{ "alert": "error", "message": "An error has occured." }'
        status_code = 500
    else:
        resp_msg = '{ "alert": "success", "message": "Your message has been sent successfully." }'
        status_code = 200

    return {
        'statusCode': status_code,
        'headers': { 'Access-Control-Allow-Origin': SITE_URL, },
        'body': resp_msg
    }