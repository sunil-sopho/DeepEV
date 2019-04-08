import sys
import csv

args = sys.argv
filename = args[1]
raw_file = '--' + ''.join(map(str,open(filename,'rb').readlines())) + '--0'

sections = []
tmp = ''
count = 0

for ch in raw_file:
    if (ch != '-'):
        tmp += ch
        if(count > 1):
            sections += [tmp]
            tmp = ''
        count = 0
    else:
         count += 1

data = sections[-1]
data = data.split('\\r\\n\'b\'')
data.pop(0)

data_tabular = []
for row in data:
    extracted = row.split()
    if(len(extracted)!=0):
        extracted.pop(0)
        extracted.pop(-1)
        data_tabular += [extracted]

directory = args[2]
with open(directory + "/" + (((filename.split('/'))[-1]).split('.'))[0] + '.csv','w') as my_csv:
    writer = csv.writer(my_csv,delimiter=',')
    writer.writerows(data_tabular)
