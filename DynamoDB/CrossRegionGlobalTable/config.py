ACCESS_KEY = ""
SECRET_KEY = ""

#US East (N. Virginia) us-east-1
read_boto_args = {'service_name': 'dynamodb',
             'region_name':'us-east-1',
            'aws_access_key_id': ACCESS_KEY,
             'aws_secret_access_key': SECRET_KEY,
}

#Asia Pacific (Mumbai) ap-south-1
write_boto_args = {'service_name': 'dynamodb',
             'region_name':'ap-south-1',
            'aws_access_key_id': ACCESS_KEY,
             'aws_secret_access_key': SECRET_KEY,
}