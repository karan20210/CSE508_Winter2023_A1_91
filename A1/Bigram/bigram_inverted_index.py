import pickle

class BigramInvertedIndexElement:
    def __init__(self, c, docId):
        self.character = c
        self.frequency = 1
        self.docIds = [docId]
    
    def increaseFreq(self, by = 1):
        self.frequency += by
    
    def addDocId(self, id):
        self.docIds.append(id)

    def printIndexElement(self):
        return(str(self.character) + ' ' + str(self.frequency) + ' -> ' + str(self.getDocIds()))             
    
    def getDocIds(self):
        return self.docIds

d = {}
for i in range(1,1401):    
    file_no = str(i).zfill(4)
    path = '../Q1_files/cranfield' + file_no
    f = open(path, 'r')
    x = []
    for z in f:
        for j in z.split("'"):
            if j.isalpha():
                x.append(j)
    
    for j in range(len(x) - 1):
        word = x[j] + ' ' + x[j+1]
        if word not in d.keys():            
            d[word] = BigramInvertedIndexElement(word, i)            
        else:
            if i not in d[word].getDocIds():
                d[word].increaseFreq()
                d[word].addDocId(i)
    
dbfile = open('BigramIndexPickle', 'ab')
pickle.dump(d, dbfile)
dbfile.close()

for i in d:
    print(d[i].printIndexElement())
