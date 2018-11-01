import boto3
import os
import sys
import argparse
from operator import itemgetter
from AwsServer import AwsServer
import getpass
from loadBalancer import ClassicELB
from describeELBs import findELBinASVapp

parser = argparse.ArgumentParser()
parser.add_argument("-u","--user",help="Enter your a-eid",required=True)
parser.add_argument("-r","--region",help="Enter the AWS region you want to search in",default="us-east-1")

args = parser.parse_args()
pwd = getpass.getpass('Please enter your a-eid password: ')
#pwd = input("Please enter your a-eid password: ")
#need to validate the password string.
#
#proxy = 'https://<a-eid>:<pwd>@entproxy.kdc.capitalone.com:8099'
proxy = 'https://'+ args.user + ':' + pwd + '@entproxy.kdc.capitalone.com:8099'
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy

#connection to AWS using the session in ~/.aws/*
session = boto3.Session(profile_name='GR_GG_COF_AWS_COFI_Prod_ProdSupport')
#Testing AWS connectivity by printing one of the s3 buckets
s3 = session.resource('s3')
for b in s3.buckets.all():
    print(b.name)
    break
print ("Connected to AWS!")

#Get the input from the user for what application he wants the instance details
Application = input("Please enter the Application's ASV Tag value you are looking for: ").upper()
print("you have entered application as: %s" % Application)
#Need to validate the application value.
#
#

#Creating an ec2 resource to describe ec2 servers with tagName ASV and value of the given Application
ec2 = session.client('ec2', region_name=args.region)
filters = [{'Name':'tag:ASV', 'Values':[Application]}]
response = ec2.describe_instances(Filters=filters)
x = {'ID':'','IP':'','state':'','name':''}

#finding the loadbalancers under the application using the application tag value.
lbsinASV = findELBinASVapp(Application,session,args)
#print ([x.elbName for x in lbsinASV])

#Creating a empty list of servers.
Servers = []

#Creating a new instance, getting it's values and adding to the list of servers under application
for instances in response['Reservations']:
    for instance in instances['Instances']:
        server = AwsServer()
        server.Id = instance['InstanceId']
        server.State = instance['State']['Name']
        server.Ip = instance['PrivateIpAddress']
        server.Tags={"Tags":[]}
        for tag in instance['Tags']:
            server.Tags["Tags"].append(tag)
            if tag['Key']=='Name':
                server.Name = tag['Value']
        server.getlistoflbsAttachedto(lbsinASV)
        Servers.append(server)

#To print the Header Row before printing the server Details
Servers[0].getDetailsHeader()

#Print all the servers under the queried Application in the specific region.
for k in Servers:
    k.getServerDetails()
