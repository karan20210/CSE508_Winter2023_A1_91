# import nltk
# from nltk.corpus import stopwords
# stopwords = stopwords.words('english')

# for i in range(1, 1401):
#     file_no = str(i).zfill(4)
#     path = 'Q1_files/cranfield' + file_no
#     f = open(path, 'r')

#     new_file = ''

#     for line in f:
#         line = line.strip()
#         new_file += line.lower()

#     new_file = nltk.word_tokenize(new_file)    

#     temp_file = []

#     for i in new_file:
#         if i in stopwords or (not i.isalpha()):
#             continue
#         temp_file.append(i)

#     f.close()    

#     f = open(path, 'w')
#     f.write(str(temp_file))