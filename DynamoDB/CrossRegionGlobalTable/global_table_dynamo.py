import boto3, time, faker
from config import read_boto_args, write_boto_args


read = boto3.resource(**read_boto_args)
write = boto3.resource(**write_boto_args)

read = read.Table("logfile")
write = write.Table("logfile")

fake = faker.Faker()

write_response = write.put_item(
    Item={
        "PK": "request#503",
        "bytessent": 3563,
        "date": "2009-07-21",
        "GSI_1_PK": "host#150.100.9.28",
        "host": "150.100.9.28",
        "hourofday": 21,
        "method": "GET",
        "requestid": 330,
        "responsecode": 200,
        "timestamp": fake.unix_time(),
        "timezone": "GMT-0700",
        "url": "/rss.pl",
        "useragent": "Baiduspider+(+http://www.baidu.com/search/spider.htm)"
        }
)


print("write response in {}: ".format(read_boto_args["region_name"]), str(write_response))

time.sleep(15)

read_respose = read.get_item(
        Key={
            "PK": "request#501",
        },
)

print("read response in {}: ".format(write_boto_args["region_name"]), str(read_respose))