import sys
import PyIO
import PyPluMA

class ZeroPercentPlugin:
    def input(self, inputfile):
       self.parameters = PyIO.readParameters(inputfile)

       self.infile = open(PyPluMA.prefix()+"/"+self.parameters["abund"], 'r')
       self.twocol = open(PyPluMA.prefix()+"/"+self.parameters["twocol"], 'r')
       self.control = self.parameters["control"]
       self.case = self.parameters["case"]

    def run(self):
       #self.numcontrol = int(sys.argv[2])
       self.samples = self.infile.readline().strip().split(',')
       self.minval = 200
       minside = ""
       self.setname = dict()
       self.numcontrol = 0
       self.numcase = 0
       self.twocol.readline()
       for line in self.twocol:
          contents = line.strip().split(',')
          self.setname[contents[0]] = contents[1]
          if (contents[1] == self.control):
             self.numcontrol += 1
          elif (contents[1] == self.case):
             self.numcase += 1

    def output(self, outputfile):
       for line in self.infile:
           contents = line.strip().split(',')
           contents = contents[1:]
           zero_control = 0
           zero_case = 0
           for i in range(1, len(contents)):
               if (float(contents[i]) == 0.0):
                   if (self.setname[self.samples[i]] == self.control):
                       zero_control += 1
                   else:
                       zero_case += 1
           pct_control = 100 - (float(zero_control)/self.numcontrol * 100)
           pct_case = 100 - (float(zero_case)/self.numcase * 100)
           if (pct_control < self.minval):
               self.minval = pct_control
               minside = self.control
           #if (pct_case < self.minval):
           #    self.minval = pct_case
           #    minside = "ADHD"

       print(minside)
       print(self.minval)
