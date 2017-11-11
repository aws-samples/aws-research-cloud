import json
import boto3
import os

# Change to 0 to enable instances stopping
DEBUG = os.environ['DebugMode']
TAGKEY = os.environ['TagKey'].lower()
TAGVALUE = os.environ['TagValue'].lower()

# Connect to EC2 service and get list of available regions
ec2client = boto3.client('ec2',region_name='us-east-1')
response = ec2client.describe_regions()

# Iterate regions
regions = []
for region_info in response['Regions']:
  regions.append(region_info['RegionName'])

# Main handler
def handler(event, context):
  # Create a filter for running instances
  filters = [
  {
    'Name': 'instance-state-name',
    'Values': ['running']
  }]

  # Iterate regions
  for region in regions:
    print("Region: " + region)

    # Connect to the AutoScaling API
    asgclient = boto3.client('autoscaling',region_name=region)

    # Describe all ASGs
    asgresp = asgclient.describe_auto_scaling_groups()
    asgs = []

    # Track instances in an ASG - we don't want to shut these down later
    i_in_asg = []

    # Loop across every ASG in the region
    for asg in asgresp['AutoScalingGroups']:
      asgmin = asg['MinSize']
      asgdes = asg['DesiredCapacity']
      asgmax = asg['MaxSize']
      asgins = asg['Instances']

      # Check for instances in that ASG
      if asgins:
        # Loop instances we've found in the ASG
        for ins in asgins:
          # Track instances in our array so we don't shut them down again
          i_in_asg.append(ins['InstanceId'])

      # Define a tag filter to allow us to grab all tags in this ASG
      asgfilter = [
        {
          'Name':'auto-scaling-group',
          'Values': [asg['AutoScalingGroupName']]
        }
      ]

      # Get all ASG tags
      asgtags = asgclient.describe_tags(Filters=asgfilter)

      # Default the action to zero the ASG
      zeroasg = 1

      # Loop over all the tags
      for tag in asgtags['Tags']:
        # If we find a tag called KeepRunning
        if tag['Key'].lower() == TAGKEY:
          if tag['Value'].lower() == TAGVALUE:
            # Keep the ASG
            zeroasg = 0
      # If ASG should be zeroed
      if zeroasg == 1:
        # Check we're not running in debug mode
        if DEBUG == 'LIVE':
          print "Zeroing ASG: " + asg['AutoScalingGroupName'] + " (from min/des/max): " + str(asgmin) + " / " + str(asgdes) + " / " + str(asgmax) + ")"
          resp = asgclient.update_auto_scaling_group(
            AutoScalingGroupName = asg['AutoScalingGroupName'],
            MinSize = 0,
            MaxSize = 0,
            DesiredCapacity = 0
          )
        else:
          print "Zeroing ASG: " + asg['AutoScalingGroupName'] + " (from min/des/max): " + str(asgmin) + " / " + str(asgdes) + " / " + str(asgmax) + ") [DEBUG] "
      else:
        print "Keeping ASG: " + asg['AutoScalingGroupName'] + " (min/des/max): " + str(asgmin) + " / " + str(asgdes) + " / " + str(asgmax) + ")"
    # Connect to the EC2 API
    ec2 = boto3.resource('ec2',region_name=region)
    # Get running instances
    instances = ec2.instances.filter(Filters=filters)
    # Iterate instances
    for i in instances:
      stopi = 1      # Assume we stop
      iname = "empty-name-tag" # Set default  name
      tags = i.tags  # Get list of tags
      # Check for tags
      if tags:
        # Look for KeepRunning tag
        for tag in tags:
          if tag['Key'].lower() == 'name':
            iname = tag['Value']
          if tag['Key'].lower() == TAGKEY:
            if tag['Value'].lower() == TAGVALUE:
              stopi = 0
      # stop instances with no tags
      else:
        iname = "no-name-tag"
        stopi = 1
      # Skip instances in ASGs
      if i.id in i_in_asg:
        print "Ignoring:    " + i.id + " (" + iname + " - " + i.instance_type + " is in an ASG)"
      # stop instances
      elif stopi == 1:
        # Check we're not DEBUG
        if DEBUG == 'LIVE':
          if i.root_device_type == "instance-store":
            print "Terminating: " + i.id + " (" + iname + " - " + i.instance_type + ")"
            i.terminate()
          else:
            print "Stopping:    " + i.id + " (" + iname + " - " + i.instance_type + ")"
            i.stop()
        else:
          print "Stopping:    " + i.id + " (" + iname + " - " + i.instance_type + ") [DEBUG] "
      else:
        print "Keeping:     " + i.id + " (" + iname + " - " + i.instance_type + ")"
