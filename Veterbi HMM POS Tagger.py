def tag(sentence):
    PreviousPercentage = 1
    SavePercentage = 0
    PreviousPOS = "S"
    SaveTag = ""
    TempPercentage = 0
    WordPercentage = 0
    POSPercentage = 0
    TagSentence = list()
    
    for word in sentence:
        # print(word+" + Prev= "+PreviousPOS)
        if word.lower() in WordDict:
            PossiblePos = WordDict[word.lower()].keys()
            
            for pos in PossiblePos:
                # print(pos)
                
                WordPercentage = WordDict[word.lower()][pos]
                    
                if PreviousPOS in POSDict[pos]:
                    POSPercentage = POSDict[pos][PreviousPOS]
                else:
                    POSPercentage = 1
                
                if PreviousPOS == "S":
                    TempPercentage = PreviousPercentage * WordPercentage
                else:
                    TempPercentage = PreviousPercentage * POSPercentage * WordPercentage
    
                if TempPercentage > SavePercentage:
                    SavePercentage = TempPercentage
                    SaveTag = pos
        else:
            SaveTag = "OOV"
            SavePercentage = 1/1000
                  
        PreviousPOS = SaveTag
        PreviousPercentage = SavePercentage
        SavePercentage = 0
        TagSentence.append(word + "\t" + SaveTag.upper() + "\n") 
    return TagSentence


trainingCorpus = open("Training Corpus.pos", "r")
WordDict = dict()
POSDict = dict()
previousPOS = "S"

# creating Word and POS dictionaries
for line in trainingCorpus:
    if line != "\n":
        line = line.lower()
        arr = line.split()
        word = arr[0]
        pos = arr[1]
        
        # Word likelihood table 
        if word not in WordDict:
            WordDict[word] = dict()
        if pos not in WordDict[word]:
            WordDict[word][pos] = 0
        WordDict[word][pos] += 1
        
        # Previous POS likelihood table
        if pos not in POSDict:
            POSDict[pos] = dict()
            POSDict[pos]["occurrences"] = 0
        if previousPOS not in POSDict[pos]:
            POSDict[pos][previousPOS] = 0 
        POSDict[pos][previousPOS] += 1
        POSDict[pos]["occurrences"] += 1
        
        previousPOS = pos
        if previousPOS == ".":
            previousPOS = "S"

trainingCorpus.close()

# turning counts into percentages
for pos in POSDict:
    for key in POSDict[pos]:
        if key != "occurrences":
            POSDict[pos][key] = POSDict[pos][key] / POSDict[pos]["occurrences"]
                    
for word in WordDict:
    for pos in WordDict[word]:
        WordDict[word][pos] = WordDict[word][pos] / POSDict[pos]["occurrences"]
        
file = input("Input a .words file to be tagged.\n")
POSfile = file[:file.find('.')]+".pos"
testCorpus = open(file, "r")
outputFile = open(POSfile, "w")

sentence = list()
for line in testCorpus:
    if line != "\n":
        sentence.append(line[:-1])  # removes \n from the end of word
    if line == ".\n":
        sentence = tag(sentence)
        for word in sentence:
            outputFile.write(word)
        outputFile.write("\n")
        sentence = list()

testCorpus.close()
outputFile.close()

print("Tagged file saved as "+POSfile)
