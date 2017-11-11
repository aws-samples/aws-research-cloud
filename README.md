# aws-research-cloud
Sample code supporting the AWS Research Cloud initiative.

## Budget Safety Switch
This is a CloudFormation template that deploys a Lambda function which, when triggered, looks through every region and stops (or, in the case of instance-backed instances, terminates) EC2 instances that don't have a KeepRunning tag set.

[Budget Safety Switch - README.md](budget-safety-switch/README.md)

[Budget Safety Switch - CloudFormation Template](budget-safety-switch/budget-safety-switch.yaml)

## Budget Safety Switch (SAM Template)
A repackaged version of the above template using the Serverless Application Model (SAM) framework.  This version also allows you to define a specific tag key/value combination for the instances you want to keep.

[Budget Safety Switch (SAM) - README.md](budget-safety-switch-sam/README.md)

[Budget Safety Switch (SAM) - CloudFormation Template](budget-safety-switch-sam/budget-safety-switch-sam.yaml)

[Budget Safety Switch (SAM) - Lambda Python Code](budget-safety-switch-sam/index.py)

For more information, please refer to the AWS Research Cloud Program documentation.
