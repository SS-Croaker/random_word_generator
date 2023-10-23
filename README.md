# random_word_generator
I want to create a random word generator, so that when a user comes to my website they can click on the button to create a random word, and then that random word would be searched in the website. This would lead to the relevant blogs being shown in the search. For this, the random word generator would have to be a keyword from my website.

How should I go about it?

Create a Python program - Stupid method
Create a WordPress plugin - An even more stupid method
Edit the WordPress theme - Something that works with the least effort

Create a Python program for web scrapping, NLP, store the keyword and random word generator

You can access the random keyword generator here

Note: Jio has blocked GitHub raw links. So the nltk.download('stopwords') and nltk.download('punkt') commands used to download the datasets/tokenizers may not work.

stopwords: This dataset provides a list of common words (like "and", "the", "is", etc.) for various languages. In the program, we use the English stopwords to filter out these common words from the extracted keywords.

punkt: This is a pre-trained tokenizer model for English. It's used by the word_tokenize function to split the text into individual words (tokens)

The file size for the punkt tokenizer is approximately 13 MB and for the stopwords dataset it often less than 1 MB.

So instead of changing DNS, using VPN or proxy, simply download it from your mobile data.

To scrape the entire website, you'll need to implement a web crawler that starts from the homepage and then follows links to other pages within the same domain.

Here's a step-by-step approach to achieve this:

Start with the homepage: Fetch the content of the homepage.
Extract all internal links: Identify all links that lead to other pages within the same domain.
Visit each link: For each extracted link, fetch the content of that page.
Repeat the process: Continue the process for each new page, ensuring not to revisit already scraped pages.

But the the program was scrapping the whole website and not just the titles of the posts, you'll need to modify the web scraping function to specifically target the HTML tags that contain the titles.

Typically, titles of pages or posts are contained within <h1>, <h2>, <h3>, etc., tags, or sometimes within <title> tags

Remember to exclude URLs containing /tag/ by adding a condition in the scrape_website_titles function

Use the urlparse function from the urllib.parse module to extract the domain of the current URL. If the domain contains "talesofss.com", the function will proceed to extract the titles from the <h1>, <h2>, and <h3> tags. Otherwise, it will skip the title extraction for that URL.

This ensures that titles are only extracted from URLs that belong to your website.

Also you would want to start with a fresh database each time you run the program, otherwise every time you run the program, the keywords extracted from the titles are added to the SQLite database. The database itself is not recreated from scratch, so the keywords from previous runs will still be present in the database.

To ensure a completely fresh start every time you run the program, you can drop the table and recreate it at the beginning of each run.

By using the set data structure, you ensure that only unique keywords and titles are passed to the database functions. And by using the INSERT OR IGNORE command in SQLite along with the UNIQUE constraint, you ensure that the database will ignore any duplicates that might still be attempted to be inserted. This combination ensures that no duplicates are stored in the database.

Finally create a function get_random_title() that fetches a random title from the titles table in the SQLite database

After creating this python program, the question of the hour is how do I integrate this with my website? I want to open the home page, create a button where user will click on "random article" Once the user clicks on random article, the code runs and it selects for 1 random title. Then the title is searched on the website.

Since your website is built on WordPress, here's a step-by-step guide to implement this:

Integrating custom Python scripts into a WordPress website is a bit more involved than with frameworks like Flask or Django. WordPress is primarily PHP-based, so you'll need to find a way to execute your Python script from within PHP. Here's a step-by-step guide to help you:

Host Your Python Script on a Server:

One of the cleanest ways to do this is by setting up a Flask or Django microservice that runs your Python script. This service can be hosted on the same server as your WordPress site or a different one.
This microservice will expose an endpoint (e.g., /random-article) that, when hit, will run the Python script and return the random title.

Call the Python Microservice from WordPress:

You can use WordPress's built-in wp_remote_get function to make a GET request to your Python microservice.
Once you get the response (i.e., the random title), you can then use it as needed within WordPress.

Integrate with WordPress:

Create a custom page template or modify an existing one in your WordPress theme.
Add a button labeled "Random Article".
Use JavaScript/jQuery to handle the button click event. When clicked, make an AJAX request to a custom WordPress AJAX action.
In your theme's functions.php file, set up the custom AJAX action to call the Python microservice using wp_remote_get and then search for the article in WordPress using WP_Query or direct SQL queries.
