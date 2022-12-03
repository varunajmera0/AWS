import boto3
from config import write_boto_args
import faker


write = boto3.resource(**write_boto_args)

write = write.Table("logfile")
fake = faker.Faker()
i = 600
while True:
    i += 1
    host = fake.ipv4()
    write_response = write.put_item(
        Item={
            "PK": "request#{}".format(i),
            "bytessent": fake.random_digit(),
            "date": "{}".format(fake.date()),
            "GSI_1_PK": "host#{}".format(host),
            "host": "{}".format(host),
            "hourofday": fake.random_digit(),
            "method": "{}".format(fake.http_method()),
            "requestid": fake.random_int(),
            "responsecode": 200,
            "timestamp": fake.unix_time(),
            "timezone": "GMT-{}".format(fake.random_int(min=4, max=4)),
            "url": "{}".format(fake.uri_path()),
            "useragent": "{}".format(fake.chrome())
            }
    )
    print("write response in {}: ".format(write_boto_args["region_name"]), str(write_response))

