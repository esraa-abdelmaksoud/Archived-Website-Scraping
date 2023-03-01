import requests
import re
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime
import json

json_path = "./posts.json"
urls = [
    "https://web.archive.org/web/20110617044601/http://www.bananasontoast.org/",
    "https://web.archive.org/web/20110617050429/http://www.bananasontoast.org/page/2/",
    "https://web.archive.org/web/20110617050938/http://www.bananasontoast.org/page/3/",
    "https://web.archive.org/web/20110617053437/http://www.bananasontoast.org/page/4/",
    "https://web.archive.org/web/20110617071758/http://www.bananasontoast.org/page/5/",
    "https://web.archive.org/web/20110617091626/http://www.bananasontoast.org/page/6/",
    "https://web.archive.org/web/20110617111010/http://www.bananasontoast.org/page/7/",
    "https://web.archive.org/web/20110617124200/http://www.bananasontoast.org/page/8/",
    "https://web.archive.org/web/20110617133103/http://www.bananasontoast.org/page/9/",
    "https://web.archive.org/web/20110617140805/http://www.bananasontoast.org/page/10/",
    "https://web.archive.org/web/20110617142508/http://www.bananasontoast.org/page/11/",
    "https://web.archive.org/web/20110617145536/http://www.bananasontoast.org/page/12/",
    "https://web.archive.org/web/20110617153747/http://www.bananasontoast.org/page/13/",
    "https://web.archive.org/web/20110617165223/http://www.bananasontoast.org/page/15/",
    "https://web.archive.org/web/20110617172631/http://www.bananasontoast.org/page/17/",
    "https://web.archive.org/web/20110617173842/http://www.bananasontoast.org/page/18/",
    "https://web.archive.org/web/20110617181701/http://www.bananasontoast.org/page/19/",
    "https://web.archive.org/web/20110617184450/http://www.bananasontoast.org/page/20/",
    "https://web.archive.org/web/20110617185331/http://www.bananasontoast.org/page/21/",
    "https://web.archive.org/web/20110617185946/http://www.bananasontoast.org/page/22/",
    "https://web.archive.org/web/20110617190150/http://www.bananasontoast.org/page/23/",
    "https://web.archive.org/web/20110617190451/http://www.bananasontoast.org/page/24/",
    "https://web.archive.org/web/20110617190518/http://www.bananasontoast.org/page/25/",
    "https://web.archive.org/web/20110617190557/http://www.bananasontoast.org/page/26/",
    "https://web.archive.org/web/20110617190623/http://www.bananasontoast.org/page/27/",
    "https://web.archive.org/web/20110617190637/http://www.bananasontoast.org/page/28/",
    "https://web.archive.org/web/20110617190712/http://www.bananasontoast.org/page/29/",
]


def write_to_file(posts_dict, json_path):
    """
    Writes a dictionary of posts to a JSON file.

    Args:
        posts_dict (dict): Dictionary containing post information.
        json_path (str): Path to the JSON file to be written.

    Returns:
        None
    """
    with open(json_path, "w") as outfile:
        json.dump(posts_dict, outfile, indent=4)
    return None


def clean_date(raw_date):
    """
    Converts a raw date string to ISO 8601 format.

    Args:
        raw_date (str): Date string in the format "Month day year".

    Returns:
        str: Date string in ISO 8601 format (yyyy-mm-ddThh:mm:ssZ).
    """
    formatted_date = str(datetime.strptime(raw_date, "%B %d %Y"))
    date = formatted_date[:10] + "T" + formatted_date[11:] + "Z"
    return date


def create_json(date, final_md):
    """
    Creates a JSON object containing metadata and a post in Simplenote format.

    Args:
        date (str): Date in ISO 8601 format.
        final_md (str): Markdown-formatted post content.

    Returns:
        dict: JSON object containing metadata and post content.
    """
    cur_dict = {
        "metadata": {"version": "1.0"},
        "entries": [
            {
                "isPinned": False,
                "uuid": "",
                "timeZone": "",
                "creationDate": date,
                "creationDeviceType": "",
                "creationOSVersion": "",
                "editingTime": 0,
                "isAllDay": False,
                "modifiedDate": date,
                "creationOSName": "",
                "text": final_md,
                "creationDeviceModel": "",
                "starred": False,
                "duration": 0,
                "creationDevice": "",
            }
        ],
    }
    return cur_dict


def scrape_urls(urls):
    """
    Scrapes blog post information from a list of URLs.

    Args:
        urls (list): List of URLs to scrape.

    Returns:
        dict: Dictionary containing information for all scraped blog posts.
    """
    posts_dict = {}
    num = 0
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.findAll("div", id=re.compile("^post-"))

        for r, result in enumerate(results):

            # Initialize output
            final_md = ""

            # Getting titles
            try:
                title_elem = result.find("h2", class_="entry-title")
                title_href = title_elem.find("a")
                title = title_href.text
            except:
                title_elem = result.find("a")
                title = title_elem["title"]
            final_md += "# " + title + "\n\n"

            # Getting category
            try:
                cat_elem = result.find("div", class_="entry-utility")
                cat_span = cat_elem.find("span", class_="cat-links")
                category = cat_span.find("a").text
                final_md += "Category: " + category + "\n"
            except:
                category = "None"
            final_md += "Category: " + category + "\n"

            # Getting date and time
            try:
                date_elem = result.find("div", class_="entry-meta")
                date_href = date_elem.find("a")
                date_span = date_href.find("span", class_="entry-date")
                date_text = date_span.text
                # Clean date for json
                raw_date = re.sub("(\d+)(st|nd|rd|th)*(,)", r"\1", date_text)
                date = clean_date(raw_date)
                final_md += "Date: " + date_text + "\n\n"

            except:
                date_elem = result.find("div", class_="entry-utility")
                date_line = date_elem.text
                init_date = re.search("on (.+?) by", date_line).group(1)
                # Clean date for md
                raw_date = re.sub("(st|nd|rd|th)*(,)", r"\2", init_date)
                # Clean date for json
                std_date = re.sub("(st|nd|rd|th)*(,)", r"", init_date)
                date = clean_date(std_date)
                final_md += "Date: " + raw_date + "\n\n"

            # Getting body
            body_elem = result.find("div", class_="entry-content")
            md_lines = md(str(body_elem)).splitlines()
            new_md_lines = []
            for i in range(len(md_lines)):
                # Strip white space at the end
                cur_md = md_lines[i].rstrip()
                if len(cur_md) != 0:
                    new_md_lines.append(cur_md)
            clean_md = "\n".join(new_md_lines)
            final_md += clean_md
            posts_dict[num] = create_json(date, final_md)
            num += 1
    return posts_dict


posts_dict = scrape_urls(urls)
write_to_file(posts_dict, json_path)
