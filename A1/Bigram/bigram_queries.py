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

dbfile = open('BigramIndexPickle', 'rb')
db = pickle.load(dbfile)


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
    a = db[words[0]].getDocIds()
    words.pop(0)
    comparisons = 0    

    for i in range(len(commands)):
        b = db[words[i]].getDocIds()
        a, c = AND(a,b)            
        comparisons += c

        # if isinstance(words[i], int):
        #     b = tup.pop(0)
        # else:
        #     b = db[words[i]].getDocIds()
        # if commands[i].upper() == 'AND':
        #     a, c = AND(a,b)            
        #     comparisons += c
        # elif commands[i].upper() == 'OR':
        #     a,c  = OR(a,b)           
        #     comparisons += c
        # else:
        #     print("Invalid Command")

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
    q = input('Enter query sentence: ')
    words = preprocess(q)

    query = ''
    for x in range(len(words) - 1):
        query = query + words[x] + ' ' + words[x+1] + ' AND '
    query = query[0:-5]
    
    answer, comparisons = execute(query)
    doc_names = ''
    for x in answer:
        doc_names += ('cranfield' + str(x).zfill(4)) + ','
        
    print("Number of documents retrieved for query " + str(i + 1) + " using bigram index: " + str(len(answer)))
    print()
    print("Names of documents retrieved for query " + str(i + 1) + " using bigram index: " + str(doc_names[:-1]))

    
