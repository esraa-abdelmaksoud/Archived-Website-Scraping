# Bananasontoast-Archived-Website-Scraping
This repository contains a Python script that scrapes certain blog posts in 27 URLs from the internet archive and saves them as JSON files in a specified directory. The script uses the requests, re, bs4, markdownify, datetime, and json modules.

## Getting Started
To use this script, follow the steps below:
Clone this repository to your local machine.
Install the required modules by running pip install -r requirements.txt in your terminal.
Modify the urls and json_path variables in the script to scrape the desired URLs and save the JSON files to the desired directory.
Run the script using the command python main.py in your terminal.

## Code Overview
The main script, main.py, contains three functions:
write_to_file(posts_dict, json_path): writes a Python dictionary to a JSON file at the specified path.
clean_date(raw_date): converts a date string to ISO 8601 format.
scrape_urls(urls): scrapes the specified URLs and saves the resulting blog posts as JSON files.

The scrape_urls(urls) function works as follows:
It loops through the URLs in the urls list.
For each URL, it makes a GET request and parses the resulting HTML with BeautifulSoup.
It finds all div elements with an id attribute starting with "post-" and loops through them.
For each post, it extracts the title and category and converts the post content from HTML to Markdown using the markdownify module.
It creates a JSON object containing the post metadata and Markdown content, and saves it to the specified file using the write_to_file function.

## Contributing
If you would like to contribute to this project, feel free to open a pull request.
