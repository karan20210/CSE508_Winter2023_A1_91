import pickle

class stuff:
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

def n_gram(n):      
    d = {}
    for i in range(1,1401):    
        file_no = str(i).zfill(4)
        path = 'Q1_files/cranfield' + file_no
        f = open(path, 'r')
        x = []
        for z in f:
            for j in z.split("'"):
                if j.isalpha():
                    x.append(j)

        for j in x:
            s = "$"+j[0]
            if s not in d.keys():
                d[s] = stuff(s,i)

            elif s in d.keys():
                if i not in d[s].getDocIds():
                    d[s].increaseFreq()
                    d[s].addDocId(i)

            s = j[-1]+"$"
            if s not in d.keys():
                d[s] = stuff(s,i)

            elif s in d.keys():
                if i not in d[s].getDocIds():
                    d[s].increaseFreq()
                    d[s].addDocId(i)
            
            for k in range(len(j)-n+1):
                s = j[k:k+n]
                if j not in d.keys():
                    if s not in d.keys():
                        d[s] = stuff(s,i)

                    elif s in d.keys():
                        if i not in d[s].getDocIds():
                            d[s].increaseFreq()
                            d[s].addDocId(i)

    return d

d = n_gram(2)
dbfile = open('invertedBigramPickle', 'ab')
pickle.dump(d, dbfile)
dbfile.close()

print(d['$x'].printIndexElement())