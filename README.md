# AWS Lambda function as contact form backend

A simple lambda function that can be used as serverless backend for static website contact forms. 

### Requirements

- Static website contact form (can be hosted in S3 or elsewhere, tested with Bootstrap 4 & JQuery form)
- AWS API gateway with lambda function proxy integration
- Use POST method and content-type: application/x-www-form-urlencoded parameters without base64 encoding
- AWS SES configured
- Lambda execution role with basic execution and SES send_raw_email permissions
- Mandatory form fields: cf-name, cf-email, cf-subject, cf-message

### Environment variables

EMAIL_SUBJECT = Email subject  
RECIPIENT = Authorised recipient in SES  
SENDER_EMAIL = Email address from an authorised domain in SES  
SITE_URL = Your site URL - this will be set as value for 'Access-Control-Allow-Origin' CORS header
