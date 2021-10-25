#!/usr/bin/python3
#   
#   Noah Olmstead Harvey, Angelina Khourisader, Griffin Lehrer, Fritz Stapfer Paz
#   
#   2021.10.20
#   
#   lixical analyzer for pl0

####  IMPORTS  #################################################################################################################

####  GLOBALS  #################################################################################################################

tokens = {                                                      #   token table (from specification document)
    "program":2,    "while":18,     "EOF":35,
    "begin":3,      "loop":19,      "var":36,
    "end":4,        "end_loop":20,  "const":37,
    ';':5,          "input":21,     "call":38,
    "declare":6,    "output":22,    "procedure":39,
    ',':7,          '+':23,         "<>":40,
    ":=":8,         '-':24,         '<':41,
    '.':9,          '*':25,         '>':42,
    "if":10,        '/':26,         ">=":43,
    "then":11,      '(':27,         "<=":44,
    "else":12,      ')':28,         "do":29,                    #   NOTE:  added "do":29 (not in documentation)
    "end_if":13,    "Real":30,
    "odd":14,       "Integer":31,
    ':':15,         "Boolean":32,
    '{':16,         '=':33,
    '}':17,         "EOL":34
}

tokenTree = {                                                   #   same token table, but as a map with starting char as key
    'E':{"EOL":34,"EOF":35},
    'I':{"Integer":31},
    'R':{"Real":30},
    'B':{"Boolean":32},
    'p':{"program":2,"procedure":39},
    'b':{"begin":3},
    'e':{"else":12,"end":4,"end_if":13,"end_loop":20},
    'd':{"do":29,"declare":6},
    'i':{"if":10,"input":21},
    't':{"then":11},
    'o':{"odd":14,"output":22},
    'w':{"while":18},
    'l':{"loop":19},
    'v':{"var":36},
    'c':{"const":37,"call":38},
    ';':{';':5},
    ',':{',':7},
    '.':{'.':9},
    ':':{':':15,":=":8},
    '{':{'{':16},
    '}':{'}':17},
    '+':{'+':23},
    '-':{'-':24},
    '*':{'*':25},
    '/':{'/':26},
    '(':{'(':27},
    ')':{')':28},
    '=':{'=':33},
    '<':{'<':41,"<>":40,"<=":44},
    '>':{'>':42,">=":43}
}

symbolTokenTree = {k:v for k,v in tokenTree.items() if(not k.isalpha())}    #   pruned tokenTree containing only non aplha keys

symbolTable = [[] for i in range(499)]                          #   499 closest prime <= 500  (only for testing (i think))

####  FUNCTIONS  ###############################################################################################################

def hasher(identifier="test", factor="pPrime", modulo=499):     ##  hasher function (pulled out of hasher script)

    hashCode = 0
    primes = [                                                  #   primes up to 1000
      2,  3,  5,  7, 11, 13, 17, 19, 23, 29,
     31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
     73, 79, 83, 89, 97,101,103,107,109,113,
    127,131,137,139,149,151,157,163,167,173,
    179,181,191,193,197,199,211,223,227,229,
    233,239,241,251,257,263,269,271,277,281,
    283,293,307,311,313,317,331,337,347,349,
    353,359,367,373,379,383,389,397,401,409,
    419,421,431,433,439,443,449,457,461,463,
    467,479,487,491,499,503,509,521,523,541,
    547,557,563,569,571,577,587,593,599,601,
    607,613,617,619,631,641,643,647,653,659,
    661,673,677,683,691,701,709,719,727,733,
    739,743,751,757,761,769,773,787,797,809,
    811,821,823,827,829,839,853,857,859,863,
    877,881,883,887,907,911,919,929,937,941,
    947,953,967,971,977,983,991,997
    ]
    fPrime = [primes[i] for i in range(30)]                     #   the first 30 primes
    lPrime = [                                                  #   the 30 largest primes <10000000
    9999463, 9999469, 9999481, 9999511, 9999533, 9999593, 9999601, 9999637, 9999653, 9999659,
    9999667, 9999677, 9999713, 9999739, 9999749, 9999761, 9999823, 9999863, 9999877, 9999883,
    9999889, 9999901, 9999907, 9999929, 9999931, 9999937, 9999943, 9999971, 9999973, 9999991
    ]
    pPrime = [primes[(prime-1)] for prime in fPrime]            #   the first 30 prime/primes (primes at prime indexes)

    if(factor not in ["fPrime","lPrime","pPrime","index","number"]):
        print("!!!!  UNKNOWN FACTOR PASSED  !!!!")
        return(None)

    for e,char in enumerate(identifier):                        #   for each char in the identifier and it's index
        if(factor=="fPrime"): hashCode+=(ord(char)*fPrime[e])   #   multiply each char by the prime at index
        elif(factor=="lPrime"): hashCode+=(ord(char)*lPrime[e]) #   multiply each char by the big prime at index
        elif(factor=="pPrime"): hashCode+=(ord(char)*pPrime[e]) #   multiply each char by the primePrime at index
        elif(factor=="index"): hashCode+=(ord(char)*e)          #   multiply each char by the index
        elif(factor=="number"): hashCode+=(ord(char)*(e+1))     #   multiply each char by the index plus one

    return(hashCode%modulo)                                     #   return the sum of those values modulo the symbol table size


def openFile(filepath="test.pl0"):                              ##  opens passed filename/filepath and returns it as a string
    with open(filepath, 'r') as f:
        programString = f.read()
    return(programString)


def preprocessor(programString = ''):                           ##  uses .replace() to add whitespace - lessening ambiguity
    print(programString)                                                                                       ##  DEBUGGING  ##
    programString += " EOF"                                     #   add end of file token to program string
    programString = programString.replace('{'," { ").replace('}'," } ").replace('('," ( ").replace(')'," ) ")
    programString = programString.replace('+'," + ").replace('-'," - ").replace('*'," * ").replace('/'," / ")
    programString = programString.replace(';'," ; ").replace(','," , ").replace('.'," . ")
    programString = programString.replace(':'," : ").replace(": ="," := ")
    programString = programString.replace('<'," < ").replace("< >","<>").replace("< =","<=")
    programString = programString.replace('>'," > ").replace("< >","<>").replace("> =",">=")
    programString = programString.replace('='," = ").replace(": = ",":=").replace("< =","<=").replace("> =",">=")
    programString = programString.replace("<>"," <> ").replace(">="," >= ").replace("<="," <= ").replace('\n'," EOL ")
    print(programString)                                                                                       ##  DEBUGGING  ##
    return(programString)


def lexilyzerTwoPass(programString = '', filepath = "test.pl0"):##  this lexilyzer uses a string cleaning preprocess step

    if(not programString):                                      #   if there is no passed program string, a file will be opened
        programString = openFile(filepath)

    programString = preprocessor(programString)                 #   adds whitespace to program string before .split()

    programTokens = programString.split()                       #   splits program string into tokens on arbitary whitespace
    tokenList = []

    for token in programTokens:                                 #   iterate through tokens
        if(token in tokens):                                    #   if the token is in the token table
            tokenList.append(str(tokens[token]))                #   add the string value of the looked up token to token string
        elif(token[0].isalpha()):                               #   else if the token starts with an alpha char
            tokenList.append("0 "+str(hasher(token)))           #   it is a symbol - hash the token and add it to token string
            symbolTable[hasher(token)].append(token)                                                           ##  DEBUGGING  ##
        else:                                                   #   else the token is a number
            tokenList.append("1 "+str(token))                   #   add the number as a prefixed string to token string
    
    return(programTokens,tokenList)                             #   returns: tokens, transcribed (translated) tokens


def lexilyzerOnePass(programString = '', filepath = "test.pl0"):##  this lexilyzer passes over the program string once 
    pass


def lexilyzer(programString = '', filepath = "test.pl0"):       ##  this function wraps either lexilyzer (syntax analyzer calls)
    programTokens,tokenList = lexilyzerTwoPass(programString,filepath)      #   currently uses two pass version
    for e,t in enumerate(programTokens): print(f"{t:<32}{tokenList[e]}")                                       ##  DEBUGGING  ##
    return(" * ".join(tokenList))                               #   returns just the token string

####  MAIN  ####################################################################################################################

def main():
    print(lexilyzer())

if(__name__=="__main__"): main()                                #   runs main if script launched from command line