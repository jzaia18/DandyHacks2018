"""
markovChain Algorithm
Author: Jeffrey Weng
"""

import random, os, releaseSpiders
from spiders import usaSpider, huffSpider

#Format Text and Create Dictionary
def build_dict(text, key, previous_Dict):
    #format for splitting
    if "?" in text:
        text = text.replace('?', ' ?')
    if "!" in text: 
        text = text.replace('!', ' !')
    if "." in text:
        text = text.replace('.', ' .')

    textList = text.split()
    associated_values = previous_Dict
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

def generate_random_key(theDict, key):
    #find random first line(Must be capital)
    random_key = list(theDict.keys())[random.randint(0, len(list(theDict.keys())) - 1)] 
    while not str(random_key[0]).isupper():
        random_key = list(theDict.keys())[random.randint(0, len(list(theDict.keys())) - 1)] 

    return random_key

#Generating Text 
def generate_text(theDict, key, sentences): 
    #add random first line to generated text
    random_key = generate_random_key(theDict, key)

    #punctuation check on the end of the first line
    last_value = random_key.split(" ")[key - 1].strip()

    if last_value == "." or last_value == "?" or last_value == "!":
        text = random_key.strip().replace(last_value, "").strip() + last_value
    else:
        text = str(random_key) + " "

    temp_str = ""
    while sentences > 0:

        #test # of sentences
        if random_key[-1] == "." or random_key[-1] == "?" or random_key[-1] == "!": 
            text += " "
            sentences -= 1
        if sentences == 0: 
            break

        #obtain random_next_key based on weights
        if random_key in theDict:
            weighted_keys = list(theDict[random_key].keys())
            print(str(len(weighted_keys)))
            for value in range(len(weighted_keys)): 
                temp_str += (str(weighted_keys[value] + " ") * int(theDict[random_key][weighted_keys[value]]))
            random_next_key = temp_str.strip().split(" ")[random.randint(0, len(temp_str.strip().split(" ")) - 1)]
        else: 
            random_key = generate_random_key(theDict, key)
 
            #punctuation check on the end of the first line
            last_value = random_key.split(" ")[key - 1].strip()

            if last_value == "." or last_value == "?" or last_value == "!":
                text += random_key.strip().replace(last_value, "").strip() + last_value
            else:
                text += str(random_key) + " "

            weighted_keys = list(theDict[random_key].keys())
            print(str(len(weighted_keys)))
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

    #Check text for punctuation again
    while True: 
        if text.find(" .") != -1: 
            text = text[:text.find(" .")] + text[text.find(" ."):].strip()
        elif text.find(" ?") != -1: 
            text = text[:text.find(" ?")] + text[text.find(" ?"):].strip()
        elif text.find(" !") != -1: 
            text = text[:text.find(" !")] + text[text.find(" !"):].strip()
        else:
            break

    return text


def generate_training_data(data, filename, key):
    for text in data: 
        with open(filename, 'r+') as file: 
            if os.stat(filename).st_size == 0: 
                file.write(str(build_dict(text, key, {})))
            else:
                new_dict = eval(file.readline().replace('\x00', "").strip())
                open(filename, "w")
                file.write(str(build_dict(text, key, new_dict)))

# def generate_articles(key, num_articles):
#     sentences = 10
#     #Assume there's already training data
#     #with open(filename, 'w') as file: 
#         #new_dict = eval(file.readline().replace('\x00', "").strip())
#         #print(generate_text(new_dict, key, sentences))

# def generate_titles(key):
#     sentences = 1
#     #Assume there's already training data
#     with open("generated_titles.txt", 'w') as file: 
#         new_dict = eval(file.readline().replace('\x00', "").strip())
#         #print(generate_text(new_dict, key, sentences))

def main():
    key = 2
    #Obama
    #obama_data.txt
    #obamaSpider.main(["http://obamaspeeches.com/"])

    filename_body = "training_data_key_2.txt"
    filename_title = "titles.txt"
    #generate_training_data(releaseSpiders.main(), filename_body, key)
    generate_training_data(usaSpider.main(["-b"]), filename_body, key)
    generate_training_data(usaSpider(["-t"]), filename_title, key)
    generate_training_data(huffSpider(["-b"]), filename_body, key)
    generate_training_data(huffSpider(["-t"]), filename_title, key)



    #test
    # text = "The dude is Obama? Bro the fish. The dog Barked! Mom bit the Cat? The dog ate John's bone!"
    # print(generate_text(build_dict(text, key, {}), key, sentences ))
    
main()