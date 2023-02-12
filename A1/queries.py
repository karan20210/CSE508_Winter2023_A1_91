import pickle
import nltk
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

class InvertedIndexElement:
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
    
def getList(x):
    print(db[x].printIndexElement())

def NOT(x):
    try:
        doc_ids = db[x].getDocIds()
    except KeyError:
        return list(range(1, 1401))
    total_docs = set(range(1, 1401))

    return list(total_docs.difference(doc_ids))

def gen_command_tokens(q):
    words = []
    commands = []
    ops = ['AND', 'OR', 'NOT']
    for i in q.split():
        if i not in ops:
            words.append(i)
        else:
            commands.append(i)
    
    return words, commands

def gen_not_tuple(words, commands):
    tup = []
    while 'NOT' in commands:
        i = commands.index('NOT')
        word = words[i]
        postings = NOT(word)
        tup.append(postings)
        commands.pop(i)
        words[i] = i
        print("\nAfter Not Processing:",commands, words)
    return tup

def operations(words, commands, tup):    
    a = db[words[0]].getDocIds()
    words.pop(0)

    for i in range(len(commands)):
        if type(words[i])==int:
            b = tup.pop(0)
        else:
            b = db[words[i]].getDocIds()

        if commands[i] == 'AND':
            a = set(a).intersection(set(b))
        elif commands[i] == 'OR':
            a = set(a).union(set(b))
        else:
            print("Invalid Command")
            
    return a

def execute(query):

    query_words, commands = gen_command_tokens(query)
    tup = gen_not_tuple(query_words, commands)
    
    # print("\nCommands:",commands)
    # print("\nQuery Words:",query_words)
    # print("\nTup:",len(tup))
    
    final_set = operations(query_words, commands, tup)        
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

dbfile = open('invertedIndexPickle', 'rb')
db = pickle.load(dbfile)

n = int(input("No of queries: "))

for i in range(n):
    q = input('Enter query sentence: ')
    words = preprocess(q)
    no_of_operations = len(words) - 1
    ops = input('Enter ' +  str(no_of_operations) +  ' operations seperated by a comma: ')
    ops = ops.split(',')
    
    query = ''
    for i in range(no_of_operations):
        query += words[i] + ' '
        query += ops[i] + ' '
    query += words[-1]
    answer = execute(query)
    doc_names = ''
    for x in answer:
        doc_names += ('cranfield' + str(x).zfill(4)) + ','

    print("Query " + str(i) +  ': ' +  query)    
    print("Number of documents retrieved for query " + str(i) + ': ' + str(len(answer)))
    print("Names of documents for query " + str(i) + ': ' + doc_names)




