import random

#Format Text and Create Dictionary
def build_dict(text, key):
    #format for splitting
    if "?" in text:
        text = text.replace('?', ' ?')
    if "!" in text: 
        text = text.replace('!', ' !')
    if "." in text:
        text = text.replace('.', ' .')

    textList = text.split()
    associated_values = {}
    word_key = ""
    #create dictionary
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
def generate_text(theDict, key): 
    #find random first line(Must be capital)
    random_key = list(theDict.keys())[random.randint(0, len(list(theDict.keys())) - 1)] 
    while not str(random_key[0]).isupper():
        random_key = list(theDict.keys())[random.randint(0, len(list(theDict.keys())) - 1)] 
    
    #punctuation check on the end of the first line
    last_value = random_key.split(" ")[key - 1].strip()

    if last_value == "." or last_value == "?" or last_value == "!":
        random_key = random_key.strip().replace(last_value, "")
        random_key = random_key.strip() + last_value

    #add random first line to generated text
    text = str(random_key) + " "
    temp_str = ""

    while random_key[-1] != "." and random_key[-1] != "?" and random_key[-1] != "!":

        #obtain random_next_key based on weights
        weighted_keys = list(theDict[random_key].keys())
        for value in range(len(weighted_keys)): 
            temp_str += (str(weighted_keys[value] + " ") * int(theDict[random_key][weighted_keys[value]]))
        random_next_key = temp_str.strip().split(" ")[random.randint(0, len(temp_str.strip().split(" ")) - 1)]
        
        #test random_next_key punctuation
        if(random_next_key == "." or random_next_key == "?" or random_next_key == "!"): 
            text = text.strip()
            text += random_next_key
        else:
            text += random_next_key + " "

        #use a new random_key based on the chosen word
        random_key = " ".join(random_key.split(" ")[1:key]) + " " + random_next_key
        random_key = random_key.strip()

        temp_str = ""
    return text

def main():
    text = "The cat ate the fish. The dog barked and bit the cat? The dog ate John's bone!"
    key = 3
    print(generate_text(build_dict(text, key), key))

main()