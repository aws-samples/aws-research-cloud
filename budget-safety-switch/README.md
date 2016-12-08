# Budget Safety Switch
This is a CloudFormation template that deploys a Lambda function which, when triggered, looks through every region and stops (or, in the case of instance-backed instances, terminates) EC2 instances that don't have a KeepRunning tag set. It also searches Auto Scaling Groups for the same tag, and sets the Min / Desired / Max instance values to 0 if it doesn't find the KeepRunning tag.

In addition to the Lambda function, the template deploys an IAM role for the Lambda function to use, and also creates an SNS topic which can trigger the function when a message is received.  This SNS topic (which is available in the CloudFormation Outputs window) can be used within the Budgets section of the AWS console to automatically trigger the Lambda function with a budget threshold is exceeded.

Since this is designed to integrate with the Budgets system, the CloudFormation tempalte should be deployed in the US-EAST-1 Region.

For more information, please refer to the AWS Research Cloud Program documentation.

[CloudFormation Template](budget-safety-switch/budget-safety-switch.yaml)

> Note that the CloudFormation template defaults to DEBUG mode, which provides a log of what it would have done, but doesn't actually stop or terminate any instances.  Once you have tested and are happy with the implications, you can perform a Stack Update and change the parameter from DEBUG to LIVE.
