import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Ensure the directory exists
model_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Simple mock dataset for Fake News Detection
# In a real project, you would load this from a CSV file (e.g., using pandas)
data = [
    ("The earth is flat and scientists have been lying to us.", "Fake"),
    ("New study shows that drinking 10 liters of soda a day is good for health.", "Fake"),
    ("Aliens have landed in New York and are drinking coffee.", "Fake"),
    ("The stock market crashed today due to unexpected alien invasion.", "Fake"),
    ("Eating chocolate every day cures all diseases instantly.", "Fake"),
    ("A new species of bird was discovered in the Amazon rainforest.", "Real"),
    ("The government has passed a new bill to improve infrastructure.", "Real"),
    ("Water is composed of two hydrogen atoms and one oxygen atom.", "Real"),
    ("The local sports team won the championship last night.", "Real"),
    ("Global temperatures have risen by 1.5 degrees over the past century.", "Real")
]

# Separate texts and labels
texts = [item[0] for item in data]
labels = [item[1] for item in data]

# 2. Build a Machine Learning Pipeline
# TF-IDF converts text to numbers, MultinomialNB is a good baseline classifier
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# 3. Train the model
print("Training model...")
model.fit(texts, labels)
print("Training complete.")

# 4. Save the model to a file (.pkl)
model_path = os.path.join(model_dir, "fake_news_model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"Model saved to {model_path}")

# Test the model quickly
test_text = ["Scientists discover water on Mars"]
prediction = model.predict(test_text)
print(f"Test Prediction for '{test_text[0]}': {prediction[0]}")
