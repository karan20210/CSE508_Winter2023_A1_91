import pickle
import nltk

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

def preprocess(s):
    s = s.strip()
    s = s.lower()
    s = nltk.word_tokenize(s)
    return s

def retrieve_documents(query):
    query_terms = query.split()
    if len(query_terms) == 1:
        return db.get(query, [])
    else:        
        query_positions = [set(db[term].getDocIds()) for term in query_terms]
        intersection = set.intersection(*query_positions)
        result = [doc_id for doc_id, _ in sorted(intersection)]
        return result
    
dbfile = open('/Users/karan/Desktop/IIITD/Acads/Sem-6/IR/Assignments/A1/Pos Index/positionalIndexPickle', 'rb')
db = pickle.load(dbfile)

n = int(input("No of queries: "))

for i in range(n):
    q = input('Enter query sentence: ')
    words = preprocess(q)
    print(words)
    positionalAnswer = retrieve_documents(q)

    positionalDocNames = ''
    for x in positionalAnswer:
        positionalDocNames += ('cranfield' + str(x).zfill(4)) + ','
 
    print("Number of documents retrieved for query " + str(i) + " using positional index: " + str(len(positionalAnswer)))
    print("Names of documents for query " + str(i) + " using positional index: " + positionalDocNames)




