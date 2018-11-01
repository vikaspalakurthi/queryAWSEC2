class AwsServer:
    def __init__(self):
        #Name is Instance name, Id is Instance Id, and State is instance state.
        self.Name = 'vikas'
        self.Id = ''
        self.State = ''
        self.Ip = ''
        # list of dictionaries as {'elbName': elbObject} and AttachedToELBName has just the names of the lb's it's attached to.
        self.AttachedTo = []
        self.AttachedToELBName = []
        # status of the instance under the LB like InService/Out-of-Service
        self.Status = []
        #Tags on the server.
        self.Tags = {}
    def getTags(self):
        print ("{:<30} {:<10}".format('Key','Value'))
        for k in self.Tags['Tags']:
            print("{:<30} {:<40}".format(k['Key'],k['Value']))
    def getDetailsHeader(self):
        print("{:<15} {:<20} {:<40} {:<15} {:<16} {:<50}".format('State', 'ID', 'Name', 'IP Address', 'Status', 'ELB'))
    def getServerDetails(self):
        #print the details in the order state,ID,name and IP
        print("{:<15} {:<20} {:<40} {:<15} {:<16} {:<50} ".format(self.State, self.Id, self.Name, self.Ip, ''.join(str([x for x in self.Status])), ''.join(str([x for x in self.AttachedToELBName]))))
    def getlistoflbsAttachedto(self,elbsinASV):
        #Find the loadbalancers the instance is attached to
        for elb in elbsinASV:
            if self.Id in elb.Instances:
                self.AttachedTo.append({elb.elbName:elb})
                self.Status = [x[self.Id] for x in elb.instanceStatus if self.Id in x]
                self.AttachedToELBName.append(elb.elbName)
#Tags sample value below
#{
#    "Tags" : [
#        {
#                "Key": "Application",
#                "Value": "PSSI Conversion Dashboard"
#        }
#    ]
#}
