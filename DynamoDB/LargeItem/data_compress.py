import boto3, time
from config import read_boto_args
import faker, zlib, uuid
from boto3.dynamodb import types

# https://lightrun.com/answers/boto-boto3-dynamodbs-binary-type-issues-with-python-3
# >>> from boto3.dynamodb.types import Binary
# >>> b = Binary(b'hello')
# >>> b
# Binary(b'hello')

# >>> print(b.value)
# b'hello'

# >>> print(b.value.decode("utf-8"))
# hello


uid = uuid.uuid4()
read = boto3.resource(**read_boto_args)
write = boto3.resource(**read_boto_args)
read = read.Table("logfile")
write = write.Table("logfile")

fake = faker.Faker()
host = fake.ipv4()
content = fake.sentence()

print("Actual content: ", content)
if len(content) > 50:
    content = zlib.compress(bytes(content.encode("utf-8")), 1)  
print("compressed content: ", content)
id = uid.hex
write_response = write.put_item(
    Item={
        "PK": "request#{}".format(id),
        "bytessent": fake.random_digit(),
        "date": "{}".format(fake.date()),
        "GSI_1_PK": "host#{}".format(host),
        "host": "{}".format(host),
        "hourofday": fake.random_digit(),
        "method": "{}".format(fake.http_method()),
        "requestid": fake.random_int(),
        "responsecode": 200,
        "timezone": "GMT-{}".format(fake.random_int(min=4, max=4)),
        "url": "{}".format(fake.uri_path()),
        "useragent": "{}".format(fake.chrome()),
        "content": content
        }
)
print("uuid", id)
time.sleep(5)
read_respose = read.get_item(
    Key={
        "PK": "request#{}".format(id),
    },
)
print(read_respose.get("Item"))
print()
if read_respose.get("Item").get("content") is not None:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/dynamodb/types.html
    if types.TypeSerializer()._is_binary(read_respose.get("Item").get("content")):
        # print(type(read_respose.get("Item").get("content")))
        print("decompressed content", zlib.decompress(read_respose.get("Item").get("content").value).decode("utf-8"))
    else:
        print("not compressed content", read_respose.get("Item").get("content"))
else:
    print("not compressed content", None)




