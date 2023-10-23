#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 01:12:15 2023

@author: saurabhsingh
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import warnings

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import sqlite3

import nltk

import time

print(nltk.data.path)
# stopwords: This dataset provides a list of common words (like "and", "the", "is", etc.) for various languages
# punkt: This is a pre-trained tokenizer model for English. It's used by the word_tokenize function to split the text into individual words (tokens)

# Check if the necessary resources are available and download if not
# if not nltk.data.find('tokenizers/punkt'):
    
    
# nltk.download('punkt')

# if not nltk.data.find('corpora/stopwords'):
# nltk.download('stopwords')

# Step 1: Web Scraping for Titles

def scrape_website_titles(base_url):
    visited_urls = set()
    urls_to_visit = [base_url]
    titles_set = set()  # Use a set to store titles
    
    
    while urls_to_visit:
        url = urls_to_visit.pop()
        
        # Check if the URL belongs to talesofss.com
        # Check if the URL belongs to talesofss.com and does not contain "/tag/"
        domain = urlparse(url).netloc
        if "talesofss.com" not in domain or "/tag/" in url:
            continue

        if url not in visited_urls:
            visited_urls.add(url)
            try:
                response = requests.get(url)
                
                # Capture warnings while parsing with BeautifulSoup
                with warnings.catch_warnings(record=True) as w:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    if w and "Some characters could not be decoded" in str(w[-1].message):
                        print(f"Decoding warning for URL: {url}")

                # Extract titles from <h1>, <h2>, and <h3> tags
                for tag in ['h1']:
                    extracted_titles = [item.get_text() for item in soup.find_all(tag)]
                    # Filter titles that are 4 words or longer and add to the set
                    titles_set.update([title for title in extracted_titles if len(title.split()) >= 4])

                # Extract internal links
                for a_tag in soup.find_all('a', href=True):
                    link = a_tag['href']
                    if link.startswith(('http://', 'https://')) and link not in visited_urls:
                        urls_to_visit.append(link)
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")

    
    # Convert the set back to a list
    titles = list(titles_set)    

    return titles



# Step 2: NLP for Keyword Extraction
def extract_keywords(titles):
    text = ' '.join(titles)
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in tokens if word not in stop_words]
    return keywords

# Step 3: Store the Keywords in SQLite Database
def store_keywords(keywords):
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS keywords (word TEXT UNIQUE)''')  # Add UNIQUE constraint
    for keyword in set(keywords):  # Use set for deduplication
        cursor.execute("INSERT OR IGNORE INTO keywords (word) VALUES (?)", (keyword,))
    conn.commit()
    conn.close()

# Step 4: Random Word Generator
def get_random_keyword():
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute("SELECT word FROM keywords ORDER BY RANDOM() LIMIT 1")
    keyword = cursor.fetchone()[0]
    conn.close()
    return keyword

def get_random_title():
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM titles ORDER BY RANDOM() LIMIT 1")
    title = cursor.fetchone()[0]
    conn.close()
    return title

def setup_keywords_table():
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS keywords")
    cursor.execute("CREATE TABLE keywords (word TEXT UNIQUE)")
    conn.commit()
    conn.close()
    
    
def get_keyword_count():
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT word) FROM keywords")
    count = cursor.fetchone()[0]
    conn.close()
    return count


# Step 3.1: Store the Titles in SQLite Database
def store_titles(titles):
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS titles (title TEXT UNIQUE)''')  # Add UNIQUE constraint
    for title in set(titles):  # Use set for deduplication
        cursor.execute("INSERT OR IGNORE INTO titles (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()

# Step 3.2: Retrieve the count of titles stored
def get_title_count():
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT title) FROM titles")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Step 3.3: Set up the titles table
def setup_titles_table():
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS titles")
    cursor.execute("CREATE TABLE titles (title TEXT UNIQUE)")
    conn.commit()
    conn.close()



if __name__ == "__main__":
    # Start the timer
    start_time = time.time()
    
    # Drop and recreate the tables at the beginning
    setup_keywords_table()
    setup_titles_table()

    # URL of your website
    url = "https://talesofss.com/"
    titles = scrape_website_titles(url)
    print("Extracted Titles:", titles)  # This line will show the extracted titles
    
    keywords = extract_keywords(titles)
    
    store_keywords(keywords)
    store_titles(titles)  # Store the titles in the database
    
    # Print the number of unique keywords and titles in the database
    keyword_count = get_keyword_count()
    title_count = get_title_count()
    print(f"Number of unique keywords in the database: {keyword_count}")
    print(f"Number of unique titles in the database: {title_count}")
    
    # Stop the timer and print the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

    for _ in range(5):
        random_keyword = get_random_keyword()
        print(f"Random Keyword: {random_keyword}")
        
        random_title = get_random_title()
        print(f"Random Title: {random_title}")     