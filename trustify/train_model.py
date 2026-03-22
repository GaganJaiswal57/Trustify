import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

data = {
    "text": [
        "This article explains climate change and environment",
        "Artificial intelligence is transforming the world rapidly",
        "The cat sat on the mat near the window",
        "AI generated paragraph example created by machine learning",
        "Humans write with emotions and personal experience",
        "Machines generate structured and repetitive content"
    ],
    "label": [0,1,0,1,0,1]
}

df = pd.DataFrame(data)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])

model = LogisticRegression(max_iter=1000)
model.fit(X, df["label"])

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained and saved successfully!")