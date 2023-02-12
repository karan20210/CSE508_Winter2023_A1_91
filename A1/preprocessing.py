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

    if i in range(1,6):
        print("File " + str(i) + " before lowercasing: ")
        printContents(f)
        print()
    
    f.close()
    f = open(path, 'r')

    for line in f:
        line = line.strip()
        new_file += line.lower()
    
    if i in range(1,6):
        print("File " + str(i) + " after lowercasing: ")
        print(new_file)
        print()

    new_file = nltk.word_tokenize(new_file) 
    if i in range(1,6):   
        print("File " + str(i) + " after tokenization: ")
        print(new_file)
        print()

    temp_file = []

    for x in new_file:
        if x in stopwords:
            continue
        temp_file.append(x)

    if i in range(1,6):
        print("File " + str(i) + " after removing stopwords: ")
        print(temp_file)
        print()

    new_file = temp_file
    temp_file = []
    for x in new_file:
        if (not x.isalpha()):
            continue
        temp_file.append(x)

    if i in range(1,6):
        print("File " + str(i) + " after removing punctuations and blank space tokens: ")
        print(temp_file)
        print()

    f.close()    

    f = open(path, 'w')
    f.write(str(temp_file))