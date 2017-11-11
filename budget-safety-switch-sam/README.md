# Budget Safety Switch (SAM)
This is a CloudFormation template, packaged in Serverless Application Model (SAM) format, that deploys a Lambda function which, when triggered, looks through every region and stops (or, in the case of instance-backed instances, terminates) EC2 instances that don't have a specific key/value pair (by default, KeepRunning=True) tag set. It also searches Auto Scaling Groups for the same tag, and sets the Min / Desired / Max instance values to 0 if it doesn't find the required tag.

In addition to the Lambda function, the template deploys an IAM role for the Lambda function to use, and also creates an SNS topic which can trigger the function when a message is received.  This SNS topic (which is available in the CloudFormation Outputs window) can be used within the Budgets section of the AWS console to automatically trigger the Lambda function with a budget threshold is exceeded.

Since this is designed to integrate with the Budgets system, the CloudFormation template should be deployed in the US-EAST-1 Region.

To deploy into your own AWS account, clone the repository, change to the budget-safety-switch-sam directory, and use the following commands from the AWS CLI:

~~~~
aws cloudformation package --template-file ./budget-safety-switch-sam.yaml --s3-bucket <your-s3-bucket> --output-template-file deploy.yaml

aws cloudformation deploy --template-file deploy.yaml --stack-name budget-safety-switch --capabilities CAPABILITY_NAMED_IAM --region us-east-1
~~~~

For more information, please refer to the AWS Research Cloud Program documentation.

[CloudFormation Template](budget-safety-switch-sam/budget-safety-switch-sam.yaml)

[Lambda Python Code](budget-safety-switch-sam/index.py)

> Note that the CloudFormation template defaults to DEBUG mode, which provides a log of what it would have done, but doesn't actually stop or terminate any instances.  Once you have tested and are happy with the implications, you can perform a Stack Update and/or change the appropriate environment variable from DEBUG to LIVE.
