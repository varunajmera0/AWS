## Amazon DynamoDB

STEP 1 - CREATE THE DYNAMODB TABLE

```
aws dynamodb create-table --table-name logfile \
--attribute-definitions AttributeName=PK,AttributeType=S AttributeName=GSI_1_PK,AttributeType=S \
--key-schema AttributeName=PK,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
--tags Key=workshop-design-patterns,Value=targeted-for-cleanup \
--global-secondary-indexes "IndexName=GSI_1,\
KeySchema=[{AttributeName=GSI_1_PK,KeyType=HASH}],\
Projection={ProjectionType=INCLUDE,NonKeyAttributes=['bytessent']},\
ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}"
```

STEP 2 - LOAD SAMPLE DATA INTO THE TABLE
Update ACCESS_KEY & SECRET_KEY > run python3 ./InitialDataLoad/load_logfile.py logfile ./InitialDataLoad/logfile.csv

> Happy Coding! :v:
