import pickle
    
posIndex = {}

class PositionalIndexElement:
    def __init__(self, term, docId):
        self.character = term
        self.frequency = 1
        self.docIds = {docId: []}
    
    def increaseFreq(self, by = 1):
        self.frequency += by

    def printIndexElement(self):
        return(str(self.character) + ' ' + str(self.frequency) + ' -> ' + str(self.getDocIds()))   

    def getDocIds(self):
        return self.docIds

    def addPos(self, id, pos):
        self.docIds[id].append(pos) 

    def addDocId(self, id):
        self.docIds[id] = []       

for i in range(1,1401):    
    file_no = str(i).zfill(4)
    path = 'Q1_files/cranfield' + file_no
    f = open(path, 'r')

    x = []
    for z in f:
        for j in z.split("'"):
            if j.isalpha():
                x.append(j)

    for pos, term in enumerate(x):
        if term not in posIndex:
            posIndex[term] = PositionalIndexElement(term, i)
        if i not in posIndex[term].getDocIds():
            posIndex[term].addDocId(i)
            posIndex[term].increaseFreq()
        posIndex[term].addPos(i, pos)

dbfile = open('positionalIndexPickle', 'ab')
pickle.dump(posIndex, dbfile)
dbfile.close()

print(posIndex['experimental'].printIndexElement())