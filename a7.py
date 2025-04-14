# Darwin Kim


import math, os, pickle, re
from typing import Tuple, List, Dict


class BayesClassifier:
    """A simple BayesClassifier implementation

    Attributes:
        pos_freqs - dictionary of frequencies of positive words
        neg_freqs - dictionary of frequencies of negative words
        pos_filename - name of positive dictionary cache file
        neg_filename - name of positive dictionary cache file
        training_data_directory - relative path to training directory
        neg_file_prefix - prefix of negative reviews
        pos_file_prefix - prefix of positive reviews
    """

    def __init__(self):
        """Constructor initializes and trains the Naive Bayes Sentiment Classifier. If a
        cache of a trained classifier is stored in the current folder it is loaded,
        otherwise the system will proceed through training.  Once constructed the
        classifier is ready to classify input text."""
        # initialize attributes
        self.pos_freqs: Dict[str, int] = {}
        self.neg_freqs: Dict[str, int] = {}
        self.pos_filename: str = "pos.dat"
        self.neg_filename: str = "neg.dat"
        self.training_data_directory: str = "movie_reviews/"
        self.neg_file_prefix: str = "movies-1"
        self.pos_file_prefix: str = "movies-5"

        # check if both cached classifiers exist within the current directory
        if os.path.isfile(self.pos_filename) and os.path.isfile(self.neg_filename):
            print("Data files found - loading to use cached values...")
            self.pos_freqs = self.load_dict(self.pos_filename)
            self.neg_freqs = self.load_dict(self.neg_filename)
        else:
            print("Data files not found - running training...")
            self.train()

    def train(self) -> None:
        """Trains the Naive Bayes Sentiment Classifier

        Train here means generates `pos_freq/neg_freq` dictionaries with frequencies of
        words in corresponding positive/negative reviews
        """
        # get the list of file names from the training data directory
        # os.walk returns a generator (feel free to Google "python generators" if you're
        # curious to learn more, next gets the first value from this generator or the
        # provided default `(None, None, [])` if the generator has no values)
        _, __, files = next(os.walk(self.training_data_directory), (None, None, []))
        if not files:
            raise RuntimeError(f"Couldn't find path {self.training_data_directory}")

        # files now holds a list of the filenames
        # self.training_data_directory holds the folder name where these files are
        # print(files)

        # stored below is how you would load a file with filename given by `filename`
        # `text` here will be the literal text of the file (i.e. what you would see
        # if you opened the file in a text editor


        # *Tip:* training can take a while, to make it more transparent, we can use the
        # enumerate function, which loops over something and has an automatic counter.
        # write something like this to track progress (note the `# type: ignore` comment
        # which tells mypy we know better and it shouldn't complain at us on this line):
        #for index, filename in enumerate(files, 1): # type: ignore
            #print(f"Training on file {index} of {len(files)}")

        
        for i in range(len(files)):

            # Storing files[i] as a string 'text', and running that string through self.tokenize() to create a new list of string values, 'token'
            text = self.load_file(os.path.join(self.training_data_directory, files[i]))
            token = self.tokenize(text)
    
            # we want to fill pos_freqs and neg_freqs with the correct counts of words from
            # their respective reviews

            # Figuring out whether the file is a negative or positive review using 'self.neg_file_prefix' and 'self.pos_file_prefix',
            # then adding the tokenized list, 'token', to the appropriate dictionary, either 'self.neg_freqs' or 'self.pos_freqs'.
            if files[i].startswith(self.neg_file_prefix): 
                self.update_dict(token,self.neg_freqs)

            elif files[i].startswith(self.pos_file_prefix): 
                self.update_dict(token,self.pos_freqs)
        print('Model Trained. Testing...')

        # Pickling the positive and negative dictionaries to the appropriate files
        self.save_dict(self.neg_freqs,self.neg_filename)
        self.save_dict(self.pos_freqs,self.pos_filename)

    def classify(self, text: str) -> str:
        """Classifies given text as positive, negative or neutral from calculating the
        most likely document class to which the target string belongs

        Args:
            text - text to classify

        Returns:
            classification, either positive, negative or neutral
        """
        # TODO: fill me out

        # Creating a new variable, TokenList, and setting that variable equal to self.tokenize(text) 
        # to get a list of the individual tokens that occur in text
        TokenList=self.tokenize(text)

        # Storing overall Positive and Negative tones of the message as 'OverallTonePositive' and 'OverallToneNegative'
        OverallTonePositive=0
        OverallToneNegative=0

        # Storing the total number of words in both lists as 'TotalWords' to use later on
        TotalWords=49652

        # Determining the total positive and negative tone values of the message
        for i in range(len(TokenList)):

            # Adding the tones of each word in the message to the total tones of the message if the word exists in BOTH dictionaries
            try:

                # Figuring out the tone of each word by checking how many times the word appears in 
                # each list then dividing that value by the total number of words in that list 
                # and taking the log of that value to find out the overall tones of the message
                OverallToneNegative+=math.log((self.neg_freqs[TokenList[i]]+1)/neg_denominator)
                OverallTonePositive+=math.log((self.pos_freqs[TokenList[i]]+1)/pos_denominator)
            except KeyError:
                pass
        
        # Determining the net tone of the message and returning that tone
        if OverallTonePositive-OverallToneNegative>0:
            OverallTone='Positive'
        else:
            OverallTone='Negative'
        
        return OverallTone

    def load_file(self, filepath: str) -> str:
        """Loads text of given file

        Args:
            filepath - relative path to file to load

        Returns:
            text of the given file
        """
        with open(filepath, "r", encoding='utf8') as f:
            return f.read()

    def save_dict(self, dict: Dict, filepath: str) -> None:
        """Pickles given dictionary to a file with the given name

        Args:
            dict - a dictionary to pickle
            filepath - relative path to file to save
        """
        #print(f"Dictionary saved to file: {filepath}")
        with open(filepath, "wb") as f:
            pickle.Pickler(f).dump(dict)

    def load_dict(self, filepath: str) -> Dict:
        """Loads pickled dictionary stored in given file

        Args:
            filepath - relative path to file to load

        Returns:
            dictionary stored in given file
        """
        print(f"Loading dictionary from file: {filepath}")
        with open(filepath, "rb") as f:
            return pickle.Unpickler(f).load()

    def tokenize(self, text: str) -> List[str]:
        """Splits given text into a list of the individual tokens in order

        Args:
            text - text to tokenize

        Returns:
            tokens of given text in order
        """
        tokens = []
        token = ""
        tokensOptomized=[]
        for c in text:
            if (
                re.match("[a-zA-Z0-9]", str(c)) != None
                or c == "'"
                or c == "_"
                or c == "-"
            ):
                token += c
            else:
                if token != "":
                    tokens.append(token.lower())
                    token = ""
                if c.strip() != "":
                    tokens.append(str(c.strip()))

        if token != "":
            tokens.append(token.lower())

# --- REMOVING ALL WORDS IN 'Sorted_stoplist.txt' FROM TOKENS ---

        # Storing all the values of 'Sorted_stoplist.txt in 'SkipWords'
        SkipWordsFile=open('Sorted_stoplist.txt','r')
        SkipWords=SkipWordsFile.readlines()

        # Removing '/n' from the end of each value of SkipWords for contingency with list 'tokens'
        for i in range(len(SkipWords)):
            SkipWords[i]=SkipWords[i][:len(SkipWords[i])-2]
        
        # Adding each value of tokens to a new list if it is not in SkipWords, then returning that new list
        for i in range(len(tokens)):
            if tokens[i] not in SkipWords:
                tokensOptomized.append(tokens[i])
        print(tokens,tokensOptomized)

        return tokensOptomized

    def update_dict(self, words: List[str], freqs: Dict[str, int]) -> None:
        """Updates given (word -> frequency) dictionary with given words list

        By updating we mean increment the count of each word in words in the dictionary.
        If any word in words is not currently in the dictionary add it with a count of 1.
        (if a word is in words multiple times you'll increment it as many times
        as it appears)

        Args:
            words - list of tokens to update frequencies of
            freqs - dictionary of frequencies to update
        """
        # TODO: your work here
        #print('Tokens to update:', words)
        #print(freqs)


        for i in range(len(words)):

            # Checking if each value of list 'words' is in the dictionary 'freq'
            if words[i] not in freqs:

                # Adding 'words[i]' to 'freqs' with a frequency of 1 if it is not already there
                freqs[words[i]]=1
            else:

                # Ticking the frequency of 'words[i]' by one within dictionary 'freqs' if it already exists there
                freqs[words[i]]=int(freqs[words[i]])+1

        #print(freqs)
# remove this line once you've implemented this method

if __name__ == "__main__":
    #uncomment the below lines once you've implemented `train` & `classify`
    b = BayesClassifier()
    a_list_of_words = ["I", "really", "like", "this", "movie", ".", "I", "hope", \
                    "you", "like", "it", "too"]
    a_dictionary = {}
    b.update_dict(a_list_of_words, a_dictionary)
    assert a_dictionary["I"] == 2, "update_dict test 1"
    assert a_dictionary["like"] == 2, "update_dict test 2"
    assert a_dictionary["really"] == 1, "update_dict test 3"
    assert a_dictionary["too"] == 1, "update_dict test 4"
    print("update_dict tests passed.")

    pos_denominator = sum(b.pos_freqs.values())
    neg_denominator = sum(b.neg_freqs.values())

    print("\nThese are the sums of values in the positive and negative dicitionaries.")
    print(f"sum of positive word counts is: {pos_denominator}")
    print(f"sum of negative word counts is: {neg_denominator}")

    print("\nHere are some sample word counts in the positive and negative dicitionaries.")
    print(f"count for the word 'love' in positive dictionary {b.pos_freqs['love']}")
    print(f"count for the word 'love' in negative dictionary {b.neg_freqs['love']}")
    print(f"count for the word 'terrible' in positive dictionary {b.pos_freqs['terrible']}")
    print(f"count for the word 'terrible' in negative dictionary {b.neg_freqs['terrible']}")
    print(f"count for the word 'computer' in positive dictionary {b.pos_freqs['computer']}")
    print(f"count for the word 'computer' in negative dictionary {b.neg_freqs['computer']}")
    print(f"count for the word 'science' in positive dictionary {b.pos_freqs['science']}")
    print(f"count for the word 'science' in negative dictionary {b.neg_freqs['science']}")
    print(f"count for the word 'i' in positive dictionary {b.pos_freqs['i']}")
    print(f"count for the word 'i' in negative dictionary {b.neg_freqs['i']}")
    print(f"count for the word 'is' in positive dictionary {b.pos_freqs['is']}")
    print(f"count for the word 'is' in negative dictionary {b.neg_freqs['is']}")
    print(f"count for the word 'the' in positive dictionary {b.pos_freqs['the']}")
    print(f"count for the word 'the' in negative dictionary {b.neg_freqs['the']}")

    print("\nHere are some sample probabilities.")
    print(f"P('love'| pos) {(b.pos_freqs['love']+1)/pos_denominator}")
    print(f"P('love'| neg) {(b.neg_freqs['love']+1)/neg_denominator}")
    print(f"P('terrible'| pos) {(b.pos_freqs['terrible']+1)/pos_denominator}")
    print(f"P('terrible'| neg) {(b.neg_freqs['terrible']+1)/neg_denominator}")

    # # uncomment the below lines once you've implemented `classify`
    print("\nThe following should all be positive.")
    print(b.classify('I love computer science'))
    print(b.classify('this movie is fantastic'))
    print("\nThe following should all be negative.")
    print(b.classify('rainy days are the worst'))
    print(b.classify('computer science is terrible'))
pass