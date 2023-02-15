import pickle
import nltk
    
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
        query_positions = [set(db[term]) for term in query_terms]
        intersection = set.intersection(*query_positions)
        result = [doc_id for doc_id, _ in sorted(intersection)]
        return result
    
dbfile = open('positionalIndexPickle', 'rb')
db = pickle.load(dbfile)

n = int(input("No of queries: "))

for i in range(n):
    q = input('Enter query sentence: ')
    words = preprocess(q)

    positionalAnswer = retrieve_documents(q)

    positionalDocNames = ''
    for x in positionalAnswer:
        positionalDocNames += ('cranfield' + str(x).zfill(4)) + ','
 
    print("Number of documents retrieved for query " + str(i) + " using positional index: " + str(len(positionalAnswer)))
    print("Names of documents for query " + str(i) + " using positional index: " + positionalDocNames)




