import nltk
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

def printContents(f):
    for i in f:
        print(i)

for i in range(1, 1401):
    file_no = str(i).zfill(4)
    path = 'Q1_files/cranfield' + file_no
    f = open(path, 'r')

    new_file = ''

    for line in f:
        line = line.strip()
        new_file += line.lower()

    new_file = nltk.word_tokenize(new_file)    

    temp_file = []

    for x in new_file:
        if x in stopwords or (not x.isalpha()):
            continue
        temp_file.append(x)

    f.close()    

    if i in range(1,6):
            print("File " + str(i) + " before preprocessing: ")
            f = open(path, 'r')     
            printContents(f)
            print()
        
    f.close()

    if i in range(1,6):
        print("File " + str(i) + " after preprocessing: ")
        print(temp_file)
        print()

    f = open(path, 'w')
    f.write(str(temp_file))