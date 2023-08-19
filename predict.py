import json
from keras.models import load_model
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.sequence import pad_sequences
import collections



# Read the files word_to_idx.pkl and idx_to_word.pkl to get the mapping between word and index
word_to_index = {}
with open ("/Users/haringoonathilake/Downloads/Neural_Image_Caption_Generator-master/word_to_idx.pkl", 'rb') as file:
    word_to_index = pd.read_pickle(file)

index_to_word = {}
with open ("/Users/haringoonathilake/Downloads/Neural_Image_Caption_Generator-master/idx_to_word.pkl", 'rb') as file:
    index_to_word = pd.read_pickle(file)



print("Loading the model...")
model = load_model('/Users/haringoonathilake/Downloads/Neural_Image_Caption_Generator-master/model_checkpoint3/model_9.h5')


test_encoding = {}
with open("/Users/haringoonathilake/Downloads/Neural_Image_Caption_Generator-master/encoded_test_features2.pkl", "rb") as file:
    test_encoding = pd.read_pickle(file)

# Generate Captions for a random image in test dataset
def predict_caption(photo):

    inp_text = "startseq"

    for i in range(38):
        sequence = [word_to_index[w] for w in inp_text.split() if w in word_to_index]
        sequence = pad_sequences([sequence], maxlen=38, padding='post')
        
        ypred = model.predict([photo, sequence])
        ypred = ypred.argmax()
        word = index_to_word[ypred]

        inp_text += (' ' + word)

        if word == 'endseq':
            break

    final_caption = inp_text.split()[1:-1]
    final_caption = ' '.join(final_caption)
    return final_caption



all_img_IDs = list(test_encoding.keys())

# Get a random image
number = np.random.randint(0, len(test_encoding))
img_ID = all_img_IDs[int(number)]
#2105756457_a100d8434e
photo = test_encoding[img_ID].reshape((1, 2048))

print("Running model to genrate the caption...")
caption = predict_caption(photo)
#original code had caption being printed after image was generated which meant we can only see the caption after image was closed

img_data = plt.imread("/Users/haringoonathilake/Downloads/Neural_Image_Caption_Generator-master/data/Images/" + img_ID + ".jpg")
print(caption)
plt.imshow(img_data)
plt.axis("off")

plt.show()
