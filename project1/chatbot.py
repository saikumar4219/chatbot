import json
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

lemmatizer=WordNetLemmatizer()
intents=json.loads(open('intents.json').read())
words=pickle.load(open('words.pkl','rb'))
classes=pickle.load(open('classes.pkl','rb'))
model=load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
  sentence_words=nltk.word_tokenize(sentence)
  sentence_words=[lemmatizer.lemmatize(word) for word in sentence_words ]
  return sentence_words 
def bag_of_words(sentence):
  sentence_words=clean_up_sentence(sentence)
  bag=[0]*len(words)
  for w in sentence_words:
    for i,word in enumerate(words):
      if word==w:
        bag[i]=1 
  return np.array(bag)
def predict_class(sentence):
  bow=bag_of_words(sentence)
  res=model.predict(np.array([bow]))[0]
  ERROR_THRESHOLD=0.25
  results=[[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
  results.sort(key=lambda x:x[1],reverse=True)
  return_list=[]
  for r in results:
    return_list.append({'intent':classes[r[0]],'probability':r[1]})
  return return_list

def get_response(intents_list,intents_json):
  tag=intents_list[0]['intent']
  list_of_intents=intents_json['intents']
  for i in list_of_intents:
    if i['tag']==tag:
      result=random.choice(i['responses'])
      break
  return result 

def write_json(data,filename="intents.json"):
  with open(filename,"w") as f:
    json.dump(data,f,indent=4)

def updatejson(tag,message):
  with open("intents.json") as json_file:
    data=json.load(json_file)
    temp=data["intents"]
    q=0
    for i in temp:
      if i["tag"] == tag:
        for k in i["patterns"]:
          if message==k:
            q=1
            break
        if q==0:
          i["patterns"].append(message)
  write_json(data)

# def write_json(data,filename="intents.json"):
#   with open(filename,"w") as f:
#     json.dump(data,f,indent=4)

# def updatejson(tag,message):
#   with open("intents.json") as json_file:
#     data=json.load(json_file)
#     temp=data["intents"]
#     for i in temp:
#       if i["tag"] == tag:
#         if message not in i["patterns"]:
#           i["patterns"].append(message)
        

#   write_json(data)

def chatbotextention(message):
  print(message)
  i=0
  ints=predict_class(message)
  for i in ints:
    print(i)
    if i['probability']>0.7:
      updatejson(i['intent'],message)
      res=get_response(ints,intents)
      i=0
      break 
    else:
      i=1
  if i==1:
    res="please enter valid input"
    
  return res



# while True:
#   message=input("")
#   ints=predict_class(message)
#   print(ints)
#   for i in ints:
#     if i['probability']>0.7:
#       updatejson(i['intent'],message)
#       res=get_response(ints,intents)
#       i=0
#       break 
#     else:
#       i=1
#   if i==1:
#     print("please enter valid input")

  


