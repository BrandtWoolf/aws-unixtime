#!/bin/bash
# Author Brandt Woolf
# Date: 2021-08-07
# Inspiration from: https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/blank-python
set -eo pipefail

# generate s3 bucket
BUCKET_ID=$(dd if=/dev/random bs=8 count=1 2>/dev/null | od -An -tx1 | tr -d ' \t\n')
BUCKET_NAME=lambda-artifacts-$BUCKET_ID

# generate stack name
STACK_NAME=unixtime-stack-$BUCKET_ID

# record file with bucket name
echo $BUCKET_NAME > bucket-name.txt

# created s3 bucket
aws s3 mb s3://$BUCKET_NAME

# clear prioir builds
rm -rf package
cd function

# create deps
pip install --target ../package/python -r requirements.txt

cd ..

# upload deps to bucket # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-cli-package.html
aws cloudformation package --template-file template.yml --s3-bucket $BUCKET_NAME --output-template-file generated-s3-template.yml

# deploy stack with s3 path
aws cloudformation deploy --template-file generated-s3-template.yml --stack-name $STACK_NAME --capabilities CAPABILITY_NAMED_IAM
