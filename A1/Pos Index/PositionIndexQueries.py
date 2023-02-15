import pickle
import nltk
from nltk.corpus import stopwords
stopwords = stopwords.words('english')


class PositionalIndexElement:
    def __init__(self, term, docId):
        self.character = term
        self.frequency = 1
        self.docIds = {docId: []}

    def increaseFreq(self, by=1):
        self.frequency += by

    def printIndexElement(self):
        return (str(self.character) + ' ' + str(self.frequency) + ' -> ' + str(self.getDocIds()))

    def getDocIds(self):
        return self.docIds

    def addPos(self, id, pos):
        self.docIds[id].append(pos)

    def addDocId(self, id):
        self.docIds[id] = []
    
    def getPosFromDoc(self, docId):
        return self.docIds[docId]

def preprocess(s):
    new = []
    s = s.strip()
    s = s.lower()
    s = nltk.word_tokenize(s)
    for i in s:
        if i in stopwords or (not i.isalpha()):
            continue
        new.append(i)
    return new

dbfile = open('positionalIndexPickle', 'rb')
db = pickle.load(dbfile)

n = int(input("No. of queries: "))

for q in range(n):
    print()
    s = input("Enter query " + str(q+1) + " : ")
    words = preprocess(s)
    print(words)

    try:
        candidate_docs = set(db[words[0]].getDocIds().keys())
    except:
        print("Number of documents retrieved for query " + str(q + 1) + " using positional index: " + '0')
        print()
        print("Names of documents retrieved for query 1 " + str(q+1) + " using positional index: ")
        exit(0)

    for i in range(1, len(words)):
        try:
            docs_of_word = db[words[i]].getDocIds().keys()
        except:
             print("Number of documents retrieved for query " + str(q + 1) + " using positional index: " + '0')
             print()
             print("Names of documents retrieved for query 1 " + str(q+1) + " using positional index: ")
             exit(0)
        candidate_docs = candidate_docs.intersection(set(docs_of_word))

    answer_docs = []

    for i in candidate_docs:
        pos_w0 = db[words[0]].getPosFromDoc(i)    
        temp_pos = set(pos_w0)
        for j in range(1, len(words)):
            pos_wj = db[words[j]].getPosFromDoc(i)        
            pos_wj = [x - 1 for x in pos_wj]
            temp_pos = temp_pos.intersection(set(pos_wj))    
            if(len(temp_pos) != 0):
                answer_docs.append(i)

    doc_names = ''
    for x in sorted(answer_docs):
        doc_names += ('cranfield' + str(x).zfill(4)) + ','

    print("Number of documents retrieved for query " + str(q + 1) + " using positional index: " + str(len(answer_docs)))
    print()
    print("Names of documents retrieved for query " + str(q+1) + " using positional index: " + str(doc_names))

# Get AND of all 3 words to get candidate docs
# Store all positions of car and then iterate over the rest tokens
# Get position of tokens[i]