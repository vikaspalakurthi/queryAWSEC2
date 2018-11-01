import boto3
from loadBalancer import ClassicELB
import argparse
import getpass
from operator import itemgetter

#Create a elb object, get its values and add it to the list of elb's under application if it is
def findELBinASVapp(Application, session, args):
    elb = session.client('elb',region_name=args.region)
    elb_list = elb.describe_load_balancers()
    elbs = {"LoadBalancerDetails":[]}
    for lb in elb_list["LoadBalancerDescriptions"]:
        elbObj = ClassicELB()
        elbObj.elb_Desc = lb
        elbObj.getelbName()
        elbObj.getInstances()
        elbObj.elb_Tags = {"Tags":[tags for tags in elb.describe_tags(LoadBalancerNames=[elbObj.elbName])["TagDescriptions"][0]["Tags"]]}
        elbObj.health_Status_Desc = elb.describe_instance_health(LoadBalancerName=elbObj.elbName)
        elbObj.getELBStatusofInstances()
        elbObj.getInstances()
        elbObj.getelbASVTag()
        elbs["LoadBalancerDetails"].append(elbObj)
    elbsinASV = []
    for e in elbs["LoadBalancerDetails"]:
        if e.elbASVTag == Application:
            elbsinASV.append(e)
    return elbsinASV
