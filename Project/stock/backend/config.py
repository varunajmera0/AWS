ACCESS_KEY = ""
SECRET_KEY = ""

#US East (N. Virginia) us-east-1
boto_args = {'region_name':'us-east-1',
             'aws_access_key_id': ACCESS_KEY,
             'aws_secret_access_key': SECRET_KEY,
}

kafka_config = {'bootstrap.servers': '<IP>:9092'} #public ip of ec2 machine