import numpy as np
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def convert_dis(distance):
	if (1 - (distance -1)* 0.1 > 0):
		return 1 - (distance -1)* 0.1
	else:
		return 0

def google_Api_get(bigram):
	# document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)
	sentiment = client.analyze_sentiment(document=bigram).document_sentiment
	print('Sentiment: {}'.format(sentiment.score))

client = language.LanguageServiceClient()

all_races = np.load("all_races.npy")
fword = np.load("fword.npy")
gender = np.load("gender.npy")
# below are dict 
hate_All = np.load("hate_All.npy").item()
racial = np.load("racial.npy").item()
# this is a list of keys of hate_All
hate_keys = hate_All.keys()

feature_vec = []
sentence = ["stupid", "indian", "taxi", "driver", "here"]
fword_index = []
special_word_index = []
offensive = 0

# feturn 1 num of special word
for i in range(len(sentence)):
	if sentence[i] in fword:
		fword_index.append(i)
	if sentence[i] in gender or sentence[i] in all_races or sentence[i] in racial.keys() or sentence[i] in hate_keys:
		special_word_index.append(i)
	# if no special word, return all zero vector
if len(special_word_index) == 0:
	feature_vec = [0,0,0,0,0]
	#break
feature_vec.append(len(special_word_index))
print(special_word_index)
print("hey")
# eturne 2 distance between special word and fword
min_dis = 100
for fword_i in fword_index:
	for special_word_i in special_word_index:
		min_dis = min(min_dis, abs(fword_i - special_word_i))


feature_vec.append(convert_dis(min_dis)

# feture 3 offensiveness
print(special_word_index)
for special_word_i in special_word_index:
	if sentence[special_word_i] in hate_keys:
		offensive += hate_All[sentence[special_word_i]]
feature_vec.append(offensive)

# dict of racial and gender
exist = 0
for special_word_i in special_word_index:
	temp = sentence[special_word_i]
	if temp in racial.keys():
		for racial_value in racial[temp]:
			if racial_value in sentence_changed:
				exist = 1
				break
feature_vec.append(exist)

# google api score
api_value = 0
for i in special_word_index:
	if i - 2 >= 0:
		left_bigram = sentence[i -2] + " " + sentence[i - 1] 
		api_value = min((google_Api_get(left_bigram), api_value)
	if i + 2 < len(sentence):
		right_bigram = sentence[i + 1] + " " + sentence[i + 2]
		api_value = min(google_Api_get(right_bigram), api_value)
if api_value > 0:
	feature_vec.append(0)
else:
	feature_vec.append(abs(api_value))

print feature_vec