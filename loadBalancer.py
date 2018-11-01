class ClassicELB:
    def __init__(self):
        #This contains the response of describe-load-balancers for this elb.
        self.elb_Desc = {}
        #Contains all the Tags for this elb
        self.elb_Tags = {}
        #COntains the response of describe-instance-health
        self.health_Status_Desc = {}
        #Describes the instances state and their current state like {'InstanceID':'InstatnceStatus'}
        self.instanceStatus = []
        #list of instanceIDs under the elb.
        self.Instances = []
        self.elbName = ''
        self.elbASVTag = 'vikas'
    def getelbName(self):
        self.elbName = self.elb_Desc["LoadBalancerName"]
    def getelb_Desc(self):
        print(self.elb_Desc)
    def getInstances(self):
        self.Instances = [x["InstanceId"] for x in self.elb_Desc["Instances"]]
    def getelbASVTag(self):
            for tg in self.elb_Tags['Tags']:
                if tg['Key'] == 'ASV':
                    self.elbASVTag = tg['Value']
    def getELBStatusofInstances(self):
        self.instanceStatus = [{x["InstanceId"]:x["State"]} for x in self.health_Status_Desc["InstanceStates"]]
