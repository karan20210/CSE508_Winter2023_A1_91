confirm = input("Are u sure u want to run extraction? ")

def printContents(f):
    for i in f:
        print(i)

if(confirm.lower() == 'y'):
    for i in range(1, 1401):
        file_no = str(i).zfill(4)
        path = 'Q1_files/cranfield' + file_no

        f = open(path, 'r')       
    
        new_text = ''
        read = False
        # i = 0
        for line in f:
            line = line.strip()
            if line == '</TITLE>' or line == '</TEXT>':
                read = False
            if read:
                new_text += (line + ' ')
            if line == '<TITLE>' or line == '<TEXT>':
                read = True
            
        f.close()

        if i in range(1,6):
            print("File " + str(i) + " before extraction: ")
            f = open(path, 'r')     
            printContents(f)
        
        f.close()
        if i in range(1,6):
            print("File " + str(i) + " after extraction: ")
            print(new_text)
        f = open(path, 'w')
        f.write(new_text)
