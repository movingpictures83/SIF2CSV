import sys
import random
random.seed(1234)

class SIF2CSVPlugin:
   def input(self, inputfile):
      myfile = open(inputfile, 'r')

      lines = []
      self.nodes = set()
      for line in myfile:
         x = line.split('\t')
         for i in range(len(x)):
            x[i] = x[i].strip()
         self.nodes.add(x[0].replace(',', ''))
         self.nodes.add(x[2].replace(',', ''))
         lines.append(x)

      self.nodes = list(self.nodes)
      self.nodes.sort()
      # Take hasMember relationships.
      # We are going to remove the first node, and add
      # relationships for all its members.
      # Same for hasComplex.
      members = dict()
      for line in lines:
         if (line[1] == "hasMember" or line[1] == "hasComponent" or line[1] == "translatedTo"):
            if (not line[0] in members):
               members[line[0]] = []
            members[line[0]].append(line[2])
            if line[0] in self.nodes:
               self.nodes.remove(line[0].replace(',', ''))
         elif (line[1] == "isA"):
            if (not line[2] in members):
               members[line[2]] = []
            members[line[2]].append(line[0]) 
            if line[2] in self.nodes:
               self.nodes.remove(line[2].replace(',', ''))
 

      self.newlines = []
      for line in lines:
         if (line[0] in members):
            if (line[1] != "hasMember" and line[1] != "hasComponent" and line[1] != "translatedTo"):
               for member in members[line[0]]:
                  self.newlines.append([member, line[1], line[2]])
         elif line[2] in members:
            if (line[1] != "isA"):
               for member in members[line[2]]:
                  self.newlines.append([line[0], line[1], member])
         elif (line[1] != "hasMember" and line[1] != "hasComponent" and line[1] != "isA" and line[1] != "translatedTo"):
            self.newlines.append(line)

   def run(self):
      self.ADJ = []
      for i in range(len(self.nodes)):
         self.ADJ.append([])
         for j in range(len(self.nodes)):
            self.ADJ[i].append(0.0)
      
      for line in self.newlines:
         i = self.nodes.index(line[0].replace(',', ''))
         j = self.nodes.index(line[2].replace(',', ''))
         if (i == j):
            self.ADJ[i][j] = 1
            self.ADJ[j][i] = 1
         elif (line[1] == "directlyIncreases"):
            self.ADJ[i][j] = 0.99
         elif (line[1] == "directlyDecreases"):
            self.ADJ[i][j] = -0.99
         elif (line[1] == "increases"):
            self.ADJ[i][j] = 0.5
         elif (line[1] == "decreases"):
            self.ADJ[i][j] = -0.5
         elif (line[1] == "positiveCorrelation"):
            self.ADJ[i][j] = 0.5
         elif (line[1] == "negativeCorrelation"):
            self.ADJ[i][j] = -0.5
         elif (line[1] == "association"):
            self.ADJ[i][j] = 0.25
         elif (line[1] == "actsIn"):
            self.ADJ[i][j] = 0.25
         else:
            print("Undefined relationship: ", line[1])

   def output(self, outputfile):
      csvfile = open(outputfile, 'w')
      csvfile.write('\"\",')
      i = 0
      for node in self.nodes:
         if (i != len(self.nodes)-1):
            csvfile.write('\"'+node+'\",')
         else:
            csvfile.write('\"'+node+'\"\n')
         i += 1

      for i in range(len(self.nodes)):
         csvfile.write('\"'+self.nodes[i]+'\",')
         for j in range(len(self.nodes)):
            csvfile.write(str(self.ADJ[i][j]))
            if (j == len(self.nodes)-1):
               csvfile.write("\n")
            else:
               csvfile.write(",")

