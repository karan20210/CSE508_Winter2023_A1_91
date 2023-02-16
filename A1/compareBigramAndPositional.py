import pickle
import nltk
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

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
    
    def getPosFromDoc(self, docId):
        return self.docIds[docId]

bigram_dbfile = open('Bigram/BigramIndexPickle', 'rb')
bigram_db = pickle.load(bigram_dbfile)

pos_dbfile = open('Pos Index/positionalIndexPickle', 'rb')
pos_db = pickle.load(pos_dbfile)

def AND(a, b):
    a = sorted(a)
    b = sorted(b)    
    comparisons = 0
    final_list = []
    pa = 0
    pb = 0
    
    while pa<len(a) and pb<len(b):
        comparisons+=1
        if(a[pa] < b[pb]):            
            pa+=1
        elif(a[pa] > b[pb]):
            pb+=1
        else:
            final_list.append(a[pa])
            pa+=1
            pb+=1
    
    return final_list, comparisons

def generate_words_and_tokens(q):
    words = []  
    for i in q.split(' AND '):
        if i.upper() != 'AND':
            words.append(i)     
    return words

def operations(words, commands):    
    a = bigram_db[words[0]].getDocIds()
    words.pop(0)
    comparisons = 0    

    for i in range(len(commands)):
        b = bigram_db[words[i]].getDocIds()
        a, c = AND(a,b)            
        comparisons += c

    return a, comparisons

def execute(query):
    query_words = generate_words_and_tokens(query)           
    commands = ['AND'] * (len(query_words) - 1)
    try:
        final_set = operations(query_words, commands)
    except:
        return [], 0
    return final_set

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

n = int(input("No of queries: "))

for i in range(n):
    query_no = i+1
    q = input('Enter query sentence: ')
    words = preprocess(q)

    # BIGRAM INDEX
    query = ''
    for x in range(len(words) - 1):
        query = query + words[x] + ' ' + words[x+1] + ' AND '
    query = query[0:-5]
    
    answer, comparisons = execute(query)
    doc_names = ''
    for x in answer:
        doc_names += ('cranfield' + str(x).zfill(4)) + ','
    
    print()
    print("Query after processing: " + query)
    print()
    print("Number of documents retrieved for query " + str(query_no) + " using bigram index: " + str(len(answer)))
    print()
    print("Names of documents retrieved for query " + str(query_no) + " using bigram index: " + str(doc_names[:-1]))
    print()

    # POS INDEX
    try:
        candidate_docs = set(pos_db[words[0]].getDocIds().keys())
    except:
        print("Number of documents retrieved for query " + str(query_no) + " using positional index: " + '0')
        print()
        print("Names of documents retrieved for query 1 " + str(i+1) + " using positional index: ")
        continue

    for x in range(1, len(words)):
        try:
            docs_of_word = pos_db[words[x]].getDocIds().keys()
        except:
             print("Number of documents retrieved for query " + str(query_no) + " using positional index: " + '0')
             print()
             print("Names of documents retrieved for query 1 " + str(i+1) + " using positional index: ")
             continue
        candidate_docs = candidate_docs.intersection(set(docs_of_word))

    answer_docs = []

    for x in candidate_docs:
        pos_w0 = pos_db[words[0]].getPosFromDoc(x)    
        temp_pos = set(pos_w0)
        for j in range(1, len(words)):
            pos_wj = pos_db[words[j]].getPosFromDoc(x)        
            pos_wj = [y - 1 for y in pos_wj]
            temp_pos = temp_pos.intersection(set(pos_wj))    
            if(len(temp_pos) != 0):
                answer_docs.append(x)

    doc_names = ''
    for x in sorted(answer_docs):
        doc_names += ('cranfield' + str(x).zfill(4)) + ','

    print("Number of documents retrieved for query " + str(query_no) + " using positional index: " + str(len(answer_docs)))
    print()
    print("Names of documents retrieved for query " + str(query_no) + " using positional index: " + str(doc_names[:-1]))

    
