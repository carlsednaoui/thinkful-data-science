from bs4 import BeautifulSoup
from collections import Counter
from collections import defaultdict
from flask import Flask, abort, jsonify, request
from io import BytesIO
import math
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag as word_type
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import re
import requests
import string

# Google vision
import google.api_core.retry as g_retry
import google.api_core.timeout as g_timeout
from google.cloud import vision
from google.cloud.vision import types
import os

path="/Users/carl/sites/google.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=path


# Helper functions to prepare category data
def create_full_category(row):
    result = row.category_1.lower()
    
    if row.category_2:
        result = result + " > " + row.category_2.lower()
    if row.category_3:
        result = result + " > " + row.category_3.lower()
    if row.category_4:
        result = result + " > " + row.category_4.lower()
    if row.category_5:
        result = result + " > " + row.category_5.lower()
    if row.category_6:
        result = result + " > " + row.category_6.lower()
    if row.category_7:
        result = result + " > " + row.category_7.lower()

    return result

def get_lookup_value(row):    
    if row.lookup_value:
        return row.lookup_value.lower().split("|")
    if row.category_7:
        return [row.category_7.lower()]
    if row.category_6:
        return [row.category_6.lower()]
    if row.category_5:
        return [row.category_5.lower()]
    if row.category_4:
        return [row.category_4.lower()]
    if row.category_3:
        return [row.category_3.lower()]
    if row.category_2:
        return [row.category_2.lower()]
    if row.category_1:
        return [row.category_1.lower()]


# Email text cleaner
lemmatizer = WordNetLemmatizer()
punctuation = r"\+|\:|\{|\\|\(|\-|\`|\<|\?|\*|\;|\_|\@|\'|\[|\}|\)|\,|\/|\"|\$|\=|\&|\]|\!|\%|\>|\^|\~|\||\.|\#"

def clean_email_text(content):
    if type(content) == float and np.isnan(content): # prevent blowup if nan
        return ""
    content = " ".join(content.split("_")) # prevents blowup if subjects are concatenated with "_"
    content = " ".join(content.split("\n"))
    content = content.encode('ascii',errors='ignore') # ignore non ascii characters
    lowered = str(content).lower()
    no_punct = re.sub(punctuation, "", lowered)
    alpha = " ".join([word for word in no_punct.split(" ") if word.isalpha()])
    nouns = " ".join([word[0] for word in word_type(alpha.strip().split(" ")) if word[1] != "VB"])
    singulars = " ".join([lemmatizer.lemmatize(word) for word in nouns.split(" ") if word.isalpha()])
    return singulars


# Content matching functions
def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def contains_word_with_counter(i, s, w):
    return (i, s.count(w))

def find_matches(text, categories_df):
    text = clean_email_text(text)
    categories = []
    
    for i, row in categories_df.iterrows():
        category_to_find = row["lookup_value"]
        for c in category_to_find:
            if contains_word(text, c):
                categories.append(contains_word_with_counter(i, text, c))
    return categories



# See which images we need to process
def get_image_size(url):
    data = requests.get(url).content
    im = Image.open(BytesIO(data))    
    return im.size

def get_images_to_analyze(guid, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    images_to_analyze = []

    for img in soup.findAll('img'):
        img_url = "https://s3.amazonaws.com/assets.mailcharts.com/emails/" + guid + "/" + img["src"]
        try:
            width, height = get_image_size(img_url)
            area = width * height
            if area > 10000:
                images_to_analyze.append(img_url)
        except:
            pass

    return images_to_analyze


def get_images_data(images):
    text_results = ""
    image_results = ""

    print("-->", len(images))
    client = vision.ImageAnnotatorClient()

    for image in images:    
        request = {'image': {'source': {'image_uri': image},}, 'features': [{'type': vision.enums.Feature.Type.LABEL_DETECTION}, {'type': vision.enums.Feature.Type.TEXT_DETECTION}]}
        # https://google-cloud-python.readthedocs.io/en/latest/core/timeout.html
        # https://google-cloud-python.readthedocs.io/en/latest/core/retry.html
        my_retry = g_retry.Retry(deadline=60)
        response = client.annotate_image(request, my_retry)

        # extract the values
        text = " ".join([l.description for l in response.text_annotations])
        label = " ".join([l.description for l in response.label_annotations])

        text_results = text_results + text + " "
        image_results = image_results + label + " "

    return (text_results, image_results)


# image_content, image_text, subject_body
WEIGHTS = {
    "subject": 0.20,
    "body": 0.10,
    "image_text": 0.25,
    "image_content": 0.45
}

def calculate_result(subject, body, image_text, image_content): 
    # Calculate weight
    subject = [(s[0], s[1]*WEIGHTS["subject"]) for s in subject]
    body = [(s[0], s[1]*WEIGHTS["body"]) for s in body]
    image_text = [(s[0], s[1]*WEIGHTS["image_text"]) for s in image_text]
    image_content = [(s[0], s[1]*WEIGHTS["image_content"]) for s in image_content]
    
    # combine all of them
    subject.extend(body)
    subject.extend(image_text)
    subject.extend(image_content)
    
    # add the results
    d = defaultdict(float)

    for i in subject:
        d[i[0]] +=i[1]

    return sorted(d.items(), key=lambda t: t[1], reverse=True)

def categorize(subject, full_text, image_text, image_content, categories_df):
    subject = find_matches(subject, categories_df)
    full_text = find_matches(full_text, categories_df)
    image_text = find_matches(image_text, categories_df)
    image_content = find_matches(image_content, categories_df)
    return calculate_result(subject, full_text, image_text, image_content)

def list_categories(results, categories_df):
    total_points = sum([result[1] for result in results])
    cutoff = total_points * 0.1
    
    categories = []
    for category_index, value in results:
        if value >= 0 and total_points > cutoff:
            categories.append((categories_df.iloc[category_index]["full_category"], value))
            total_points = total_points - value
    return categories



app = Flask(__name__)

@app.route('/api', methods=['POST'])
def make_predict():
    # all kinds of error checking should go here
    data = request.get_json(force=True)
    
    # extract data
    subject = clean_email_text(data["subject"])
    full_text = clean_email_text(data["full_text"])
    guid = data["guid"]

    # create category DF
    categories_df = pd.read_csv("./data/taxonomy-carl.csv", encoding="ISO-8859-1", dtype=str)
    categories_df.fillna(False, inplace=True)
    categories_df["full_category"] = categories_df.apply(lambda x: create_full_category(x), axis=1)
    categories_df["lookup_value"] = categories_df.apply(lambda x: get_lookup_value(x), axis=1)

    url = "https://s3.amazonaws.com/assets.mailcharts.com/emails/" + guid + "/index.html"
    images = get_images_to_analyze(guid, url)
    image_text, image_content = get_images_data(images)
    print("https://www.mailcharts.com/emails/" + guid)

    results_index = categorize(subject, full_text, image_text, image_content, categories_df)
    result = list_categories(results_index, categories_df)

    return jsonify(results=result)

if __name__ == '__main__':
    app.run(port = 9000, debug = True)
