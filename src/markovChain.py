text = "The cat ate the fish. The dog barked and bit the cat? The dog ate John's bone!"
text1 =  "The cat ate the fish. The dog barked and bit the cat? The dog ate John's bone! The cat ate a potato."
associated_values = {}

#Format Text and Create Dictionary
def build_dict(text, key):
    if "?" in text:
        text = text.replace('?', ' ?')
    if "!" in text: 
        text = text.replace('!', ' !')
    if "." in text:
        text = text.replace('.', ' .')

    textList = text.split(" ")
    associated_values = {}
    word_key = ""
    for i in range(len(textList) - (key)):
        for value in range(key):
            word_key += textList[i + value] + " "
        word_key = word_key.strip()
        if word_key in associated_values: 
            if textList[i + key] in associated_values[word_key]:
                associated_values[word_key][textList[i + key]] += 1
            else: 
                associated_values[word_key][textList[i + key]] = 1 
        else: 
            associated_values[word_key] = {textList[i + key]: 1}
        word_key = ""
    return associated_values

#Generating Text 
    

print(build_dict(text1, 3))
