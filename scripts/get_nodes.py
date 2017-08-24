import boto3
import sys

region = None
asgname = None
label = None
pubhostname = None

if len(sys.argv) == 4:
    region = sys.argv[1]
    asgname = sys.argv[2]
    label = sys.argv[3]

elif len(sys.argv) == 5:
    region = sys.argv[1]
    asgname = sys.argv[2]
    label = sys.argv[3]
    pubhostname = sys.argv[4]


    #print ("Tag: " + label)
    #print ("Region : " + region)
    #print ("AutoScalingGroup: " + asgname)
else:
    print ("Must provide: <region> <asgname> <label>")
    sys.exit()


def get_asg_nodes(asgname, region):
    client = boto3.client('autoscaling', region_name=region)
    nodes = []
    combined_list = []
    asginfo = client.describe_auto_scaling_instances()

    for node in asginfo['AutoScalingInstances']:
        if node['AutoScalingGroupName'] == asgname:
            nodes.append(node['InstanceId'])
    return nodes

def get_ip_address(instanceid, region, label):
    nodes = []
    client = boto3.client('ec2',region_name=region)
    response = client.describe_instances()

    for r in response['Reservations']:
        for i in r['Instances']:
            if i['InstanceId'] == instanceid:
                    for n in i['NetworkInterfaces']:
                        nodes.append(n['PrivateDnsName'])

    return nodes

if __name__ == '__main__':
    nodeids = get_asg_nodes(asgname, region)
    print ("[{}]".format(label))
    for node in nodeids:
        n = get_ip_address(node, region, label)
        for hostname in n:
            print (hostname)