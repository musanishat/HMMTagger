#classes
class POS:
    def __init__(self, name, possibilities, data):
        self.name = name
        self.PreviousProbabilities = possibilities
        self.occurences = 0
        
        counter = 0 #counts the total POS appearences
        for previous, current in zip(data, data[1:]):
            tab= current.find('\t')
            POSTag = current[tab+1:len(current)-1]
            if POSTag == self.name:
                tab= previous.find('\t')
                POSTag = previous[tab+1:len(previous)-1]
                if POSTag == "":
                    POSTag = "."
                self.PreviousProbabilities[POSTag]+=1
                counter+=1
        self.occurences = counter       
        #turns counts into percentages
        for key in self.PreviousProbabilities:
            if counter != 0:
                self.PreviousProbabilities[key] = self.PreviousProbabilities[key]/counter

    def PreviousTagPercent(self, tag):
        return self.PreviousProbabilities[tag]

class Word:
    def __init__(self, name, POSDict, POSList, data):
        self.name = name
        self.POSProbabilities = POSDict
                        
    def incPOS(self, POSName):
        self.POSProbabilities[POSName]+=1

    def dividePOS(self):
        #turns counts into percentages
        for key in self.POSProbabilities:
            P = POSList[0]
            for i in range(0, len(POSList)):
                if POSList[i] == key:
                    P = POSList[i]
                    break
            count = P.occurences
            if count != 0:               
                self.POSProbabilities[key] = self.POSProbabilities[key]/count

class TagWord:
    def __init__(self, name, Word):
        self.name = name
        self.tag = ""
        self.POSProbabilities = Word.POSProbabilities
        print(Word.POSProbabilities)
        self.POSDiscard = list()

    def SetLikeliestTag(self):
        if(self.tag!=""):
            self.POSDiscard = self.tag
        maximum = 0
        for key in self.POSProbabilities:
            #print(self.POSProbabilities[key])
            if self.POSProbabilities[key]>maximum and key not in self.POSDiscard:
                print(here)
                tag = key.name
        if maximum==0:
            return False
        return True

class TagSentence:
    def __init__(self, sentence, POSDict, POSList, WordPOSPercentages):

        self.sentence=sentence
        sentence[0].SetLikeliestTag()
        hasTagsToTest = True
        maxPercent = 0
        saveTag = ""
        
        while hasTagsToTest:
            index = 0
            for i in range(0, len(POSList)):
                if POSList[i].name == sentence[0].tag:
                    index = i
                
            prevPOSPercent = POSList[index].PreviousTagPercent(".")
            temp = prevPOSPercent*sentence[0].POSProbabilities[sentence[0].tag]
            if temp>maxPercent:
                maxPercent = temp
                saveTag = sentence[0].tag
            
            hasTagsToTest = sentence[0].SetLikeliestTag()
        print("save: "+ saveTag)
        sentence[0].tag = saveTag
        
        for previous, current in zip(sentence, sentence[1:]):
            hasTagsToTest = True
            current.SetLikeliestTag()
            while hasTagsToTest:
                prevPOSPercent = current.tag.PreviousTagPercent(previous.tag.name)
                temp = percent*prevPOSPercent*current.POSProbabilities[current.tag]
                if temp>maxPercent:
                    maxPercent = temp
                    saveTag = current.tag
                hasTagsToTest = current.SetLikeliestTag()
            current.tag = saveTag
            

#methods
def tag(sentence, POSList, POSDict, WordPOSPercentages, WordList):
    for word in WordPOSPercentages:
        print(word.name)
    
    ToTagSentence = list()
    for word in sentence:
        #if word in WordList:
        for i in range(0, len(WordPOSPercentages)):
            if WordPOSPercentages[i].name == word:
                #print(WordPOSPercentages[i].name)
                #print(word)
                index = i
        #print(WordPOSPercentages[i])
        tempWord = TagWord(word, WordPOSPercentages[i])
        ToTagSentence.append(tempWord)
    TaggedSentence = TagSentence(ToTagSentence, POSDict, POSList, WordPOSPercentages)
    return TaggedSentence
    
#main
trainingCorpus = open("test.pos", "r")

POSDict = dict()
WordList = list()
WordPOSPercentages = list()
WordDict = dict()
data = list()

#processing POS and words
for line in trainingCorpus: #creates a dictionary of all POS in training doc
                            #and sets their probabilities to 0
    if line != "":      
        tab= line.find('\t')
        
        word = line[:tab].lower()
        if not word.isdigit():      
            if word not in WordList:
                WordList.append(word)
        POSTag = line[tab+1:len(line)-1]
        if POSTag not in POSDict and POSTag!=" " and POSTag!= "":
            POSDict[POSTag]=0
        data.append(line)

POSList=list()
for key in list(POSDict.keys()):
    temp= POS(key, POSDict, data)
    POSList.append(temp)


for line in data:
    tab= line.find('\t')
    word = line[:tab]
    POSTag = line[tab+1:len(word)-1]
    isIn=False
    for element in WordPOSPercentages:
        if element.name==word:
            isIn = True
    if not isIn:
        temp= Word(word, POSDict, POSList, data)
        WordPOSPercentages.append(temp)
        print(word)
    else:
        WordPOSPercentages[WordPOSPercentages.index(word)].incPOS(POSTag)

for word in WordPOSPercentages:
    word.dividePOS()
    
#Viterbi HMM POS tagger
print("beginning analysis")
testCorpus = open("WSJ_24.words", "r")
testCorpusPOS = open("Results.POS", "w")

sentence=list()
for line in testCorpus:
    if line[0]==" " or line[0]=="":
        continue
    line = line.replace('\n', '')
    sentence.append(line)
    if(line[0] == "." or line[0] == "?" or line[0] == "!"):
        temp = tag(sentence, POSList, POSDict, WordPOSPercentages, WordList)
        for word in temp:
            testCorpus.write(word.name+"\t"+word.tag+"\n")
        testCorpus.write(" \n")
        #sentence = list()

        
                
