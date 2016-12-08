# aws-research-cloud
Sample code supporting the AWS Research Cloud initiative.

## Budget Safety Switch
This is a CloudFormation template that deploys a Lambda function which, when triggered, looks through every region and stops (or, in the case of instance-backed instances, terminates) EC2 instances that don't have a KeepRunning tag set.

[Budget Safety Switch - README.md](budget-safety-switch/README.md)

[Budget Safety Switch - CloudFormation Template](budget-safety-switch/budget-safety-switch.yaml)

For more information, please refer to the AWS Research Cloud Program documentation.
