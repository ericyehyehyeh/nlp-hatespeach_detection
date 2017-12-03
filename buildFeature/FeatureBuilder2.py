import numpy as np
import pandas as pd
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from fuzzywuzzy import fuzz
import time

def convert_dis(distance):
    if (1 - (distance -1)* 0.1 > 0):
        return 1 - (distance -1)* 0.1
    else:
        return 0
    
def nlp_API(text, client):
    text = text
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document=document).document_sentiment

    return sentiment.score


client = language.LanguageServiceClient()    
all_races = np.load("all_races.npy", encoding="bytes")
fword = list(np.load("fword.npy",encoding="bytes"))
gender = ['men','woman','lesbian','gay','bisexual','transgender','Trans','queer',
            'questioning','intersex','lebians','gays', 'bastard','bastards', 'homo']
pronoun = ['you', 'he', 'she', 'him', 'her','your','they', 'them', 'yourself','yourselves', 'themselves', 'herself', 'himself', 'youre', 'youll', 'ur']
# below are dict 
hate_All = np.load("hate_All.npy", encoding="bytes").item()
hate_All['nigga'] = hate_All['nigger']
hate_All['dykes'] = hate_All['dyke']
hate_All['fags'] = hate_All['fag']
hate_All['hoe'] = hate_All['hoes']
racial = np.load("racial.npy", encoding="bytes").item()
# this is a list of keys of hate_All
hate_keys = list(hate_All.keys())
print (fword)
file = open("cleandata", 'r')
sentences = []
label_true = []
count = 0
for line in file:
    # print (line)
    if line.split("-")[0] == '3':
        label_true.append(1)
    else:
        label_true.append(0)
    if len(line.split("-")) < 2:
        sentences.append("")
    else:
        sentences.append(line.split("-")[1].split())

with open("label.txt", 'w') as f:
    for i in label_true:
        f.write(str(i) + '\n')
# count = 1
# print (len(sentences))
with open("feature.txt", 'w') as f:
    for sentence in sentences[:]:
        # print(sentence)
        sentence_changed = ' '.join(sentence)
        count += 1
        fword_index = []
        special_word_index = []
        pronoun_index = []
        feature_vec = []
        for i in range(len(sentence)):
            if sentence[i] in fword:
                fword_index.append(i)
            if sentence[i] in gender or sentence[i] in all_races or sentence[i] in racial.keys() or sentence[i] in hate_keys:
                special_word_index.append(i)
            if sentence[i] in pronoun:
                pronoun_index.append(i)
        # print (special_word_index)
            # if no special word, return all zero vector
        if len(special_word_index) == 0:
            feature_vec = [0,0,0,0,0,0,0]
            # print ("running")
            # print(feature_vec)
            # break
        else:
            time.sleep(0.2)
            
            # <----------------------->
            # feauture 1: length of special word
            feature_vec.append(len(special_word_index) * 1.00 /len(sentence))
            
            # <----------------------->
            # feauture 2: length of fword
            feature_vec.append(len(fword_index) * 1.00 /len(sentence))

            # <----------------------->
            # feauture 3: distance of pronoun and (fowrd or special word)
            min_dis = 100
            for i in pronoun_index:
                for fword_i in fword_index:
                    min_dis = min(min_dis, abs(fword_i - i))
                for special_word_i in special_word_index:
                    min_dis = min(min_dis, abs(special_word_i - i))

            feature_vec.append(convert_dis(min_dis))

            # <----------------------->
            # feauture 4: distance of fowrd and special word
            min_dis = 100
            for fword_i in fword_index:
                for special_word_i in special_word_index:
                    if(fword_i != special_word_i):
                        min_dis = min(min_dis, abs(fword_i - special_word_i))
            feature_vec.append(convert_dis(min_dis))

            # <----------------------->
            # feauture 5: offensiveness
            offensive = 0.0
            for special_word_i in special_word_index:
                if sentence[special_word_i] in hate_keys:
                    offensive = max(offensive, float(hate_All[sentence[special_word_i]]))
            feature_vec.append(offensive)

            # <----------------------->
            # feauture 6: if value of hate speech word exists
            exist = 0
            for special_word_i in special_word_index:
                temp = sentence[special_word_i]
                if temp in racial.keys():
                    for racial_value in racial[temp]:
                        racial_value = racial_value.lower()
                        if fuzz.partial_ratio(racial_value, sentence_changed) >= 0.88:
                            exist = 1
                            break
            feature_vec.append(exist)

            # <----------------------->
            # feauture 7: value of google api
            api_value = 0
            for i in special_word_index:
                if i - 3 >= 0:
                    left_bigram = sentence[i -3] + ' ' + sentence[i - 2] + ' ' + sentence[i - 1]  
                elif i - 2 >= 0:
                    left_bigram = sentence[i -2] + ' ' + sentence[i - 1] 
                    api_value = min(nlp_API(left_bigram, client), api_value)
                elif i - 1 == 0:
                    left_bigram = sentence[i - 1] 
                    api_value = min(nlp_API(left_bigram, client), api_value)
                if i + 3 <len(sentence) - 3:
                    right_bigram = sentence[i + 1] + ' ' + sentence[i + 2] + ' ' + sentence[i + 3]
                elif i + 2 < len(sentence) - 3:
                    right_bigram = sentence[i + 1] + ' ' + sentence[i + 2]
                    api_value = min(nlp_API(right_bigram, client), api_value)
                elif i + 1 < len(sentence) - 3:
                    right_bigram = sentence[i + 1]
                    api_value = min(nlp_API(right_bigram, client), api_value)
            if api_value > 0:
                feature_vec.append(0)
            else:
                feature_vec.append(abs(api_value))
        f.write(str(feature_vec[0])+ ' ' + str(feature_vec[1]) + ' ' + str(feature_vec[2]) + ' ' + str(feature_vec[3])+ ' ' + str(feature_vec[4]) + ' ' + str(feature_vec[5]) + ' ' + str(feature_vec[6]) + '\n')
        # print(feature_vec)
    
    # print()
