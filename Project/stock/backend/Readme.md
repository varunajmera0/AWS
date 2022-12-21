# Instructions

1. change the public ip of ec2 machine in config.py

2. copy & paste ACCESS_KEY & SECRET_KEY of AWS IAM User in config.py

3. create s3 bucket - _**stock-bronze-layer**_

4. run on terminal/cmd - pip install -r requirements.txt

5. run on terminal/cmd - flask --app stock_symbol_price.py --debug run

6. run on terminal/cmd - flask --app stock_consumer.py --debug run -p 5002
