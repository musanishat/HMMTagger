This is a very simple program to run:
1. Ensure "WSJ_02-21.pos" is in the folder to use as a training corpus.
2. Open “mn2332_HMMTrainerAndTagger_HW3.py”.
3. Input the [FILENAME].words file that you want tagged.
4. The tagged results will be placed into a file called [FILENAME].pos. 


I used a very simple implementation for OOV. 
They are tagged as OOV and the previous tag percentage for the next word is automatically set as 1/1000. 


Everything else is very self explanatory. 
This implementation uses two dimensional dictionaries to create likelihood tables.

WordList is a dictionary of words; 
each word key’s value is a dictionary of POS tags whose values are their likelihood of being the tag for that word.

POSList is a dictionary of POS tags;
each tag key’s value is a dictionary of POS tags whose values are their likelihood of being the previous tag
for that specific tag key. 

These two tables are used via the Vertebi Algorithm to probabilistically find the 
highest likelihood POS tag for each word.