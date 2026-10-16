# BeautifulSoup Basics Cheat Sheet

## Setup

```bash
pip install beautifulsoup4 requests lxml
```

```python
from bs4 import BeautifulSoup
import requests
```

## 1. Creating a soup object

```python
html = requests.get("https://example.com").text
soup = BeautifulSoup(html, "html.parser")
```

- `BeautifulSoup(markup, parser)` parses HTML into a tree you can search.
- Common parsers: `"html.parser"` (built in, no install), `"lxml"` (fast, lenient), `"html5lib"` (slowest, most browser-like), `"xml"` (for XML, needs lxml).

You can also parse a local file:

```python
with open("page.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")
```

## 2. Viewing the document

```python
print(soup.prettify())   # indented, readable HTML
print(soup.title)        # <title>...</title>
print(soup.title.string) # text inside the title tag
```

`prettify()` is great for inspecting structure while you work out what to search for.

## 3. Accessing tags directly

```python
soup.title       # first <title> tag
soup.h1          # first <h1>
soup.a           # first <a>
soup.body.p      # first <p> inside <body>
```

Dot notation returns only the **first** matching tag. Use `find_all()` for every match.

## 4. Tag properties

```python
tag = soup.a

tag.name         # 'a'  (the tag name)
tag.attrs        # {'href': '...', 'class': [...]} (dict of all attributes)
tag["href"]      # value of one attribute (KeyError if missing)
tag.get("href")  # same, but returns None if missing (safer)
tag.get("href", "default")  # with a fallback value
```

Note that `class` is a multi-valued attribute, so it returns a list: `['btn', 'primary']`.

## 5. Getting text

```python
tag.text                 # all text inside, including nested tags
tag.get_text()           # same as .text
tag.get_text(strip=True) # strips leading/trailing whitespace
tag.get_text(" ", strip=True)  # joins text pieces with a space separator
tag.string               # text only if the tag has exactly one string child, else None
list(tag.stripped_strings)  # list of all text pieces, whitespace-trimmed
```

`get_text(" ", strip=True)` is usually the cleanest option for scraped text.

## 6. Searching: `find()` and `find_all()`

```python
soup.find("div")                     # first <div>
soup.find_all("div")                 # list of all <div>s
soup.find_all(["h1", "h2", "h3"])    # match any tag in a list
soup.find_all(True)                  # every tag in the document
```

**Filter by attributes:**

```python
soup.find("div", class_="content")        # class_ (underscore, since class is reserved)
soup.find("div", id="main")
soup.find("a", href="https://example.com")
soup.find("input", attrs={"name": "email"})   # use attrs for unusual names (data-*, etc.)
soup.find_all("a", href=True)             # only <a> tags that have an href
```

**Filter by text:**

```python
soup.find_all("a", string="Click here")           # exact text match
soup.find_all("a", string=lambda s: s and "buy" in s.lower())  # custom condition
```

**Limit results:**

```python
soup.find_all("p", limit=5)               # stop after 5 matches
soup.find_all("div", recursive=False)     # only direct children, not nested
```

**Using regex or functions:**

```python
import re
soup.find_all("a", href=re.compile(r"^https://"))   # regex on attribute
soup.find_all(re.compile(r"^h[1-6]$"))              # regex on tag name

def has_class_but_no_id(tag):
    return tag.has_attr("class") and not tag.has_attr("id")
soup.find_all(has_class_but_no_id)                  # custom function filter
```

`find()` returns `None` if nothing matches, so check before accessing attributes on the result.

## 7. CSS selectors: `select()` and `select_one()`

```python
soup.select("p")                    # all <p>
soup.select("div.content")          # <div class="content">
soup.select("#main")                # element with id="main"
soup.select("ul > li")              # <li> that are direct children of <ul>
soup.select("div p")                # <p> anywhere inside a <div>
soup.select("a[href]")              # <a> with an href attribute
soup.select('a[href^="https"]')     # href starts with "https"
soup.select('a[href$=".pdf"]')      # href ends with ".pdf"
soup.select('a[href*="example"]')   # href contains "example"
soup.select("li:nth-of-type(2)")    # second <li> among siblings
soup.select_one("h1")               # first match only (None if none)
```

If you know CSS, `select()` is often shorter and more readable than chained `find()` calls.

## 8. Navigating the tree

**Down (to children):**

```python
tag.contents          # list of direct children (including text nodes)
tag.children          # iterator over direct children
tag.descendants       # iterator over all nested elements, recursively
```

**Up (to parents):**

```python
tag.parent            # the immediate parent tag
tag.parents           # iterator over all ancestors up to the document root
tag.find_parent("div")  # nearest ancestor matching a filter
```

**Sideways (siblings):**

```python
tag.next_sibling            # next node at the same level (often a "\n" text node!)
tag.previous_sibling
tag.find_next_sibling("p")  # next sibling that is a <p>
tag.find_previous_sibling("p")
tag.find_next_siblings("p") # all following <p> siblings
```

**Document order (ignores nesting):**

```python
tag.find_next("p")    # next <p> anywhere after this tag in the document
tag.find_previous("h2")
```

Whitespace between tags counts as a text node, so `next_sibling` often returns `"\n"`. Prefer `find_next_sibling()`.

## 9. Modifying the soup

```python
tag["href"] = "https://new-url.com"   # change an attribute
tag["class"] = "new-class"            # set/replace class
del tag["id"]                         # remove an attribute

tag.string = "New text"               # replace contents with text
tag.name = "span"                     # rename the tag

new = soup.new_tag("a", href="https://x.com")
new.string = "Link"
tag.append(new)                       # add as last child
tag.insert(0, new)                    # insert at position 0
tag.insert_before(new)                # place before tag
tag.insert_after(new)                 # place after tag

tag.decompose()                       # remove tag and destroy it
tag.extract()                         # remove tag but keep/return it
tag.clear()                           # remove everything inside the tag
tag.replace_with(new)                 # swap tag for another
tag.wrap(soup.new_tag("div"))         # wrap tag in a new tag
tag.unwrap()                          # remove the tag but keep its contents
```

## 10. Saving the result

```python
str(soup)                  # HTML as a string
soup.prettify()            # indented HTML string

with open("out.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())
```

## 11. Common patterns

**Extract all links:**

```python
for a in soup.find_all("a", href=True):
    print(a.get_text(strip=True), a["href"])
```

**Resolve relative URLs:**

```python
from urllib.parse import urljoin
full_url = urljoin("https://example.com/page/", a["href"])
```

**Extract a table into rows:**

```python
rows = []
for tr in soup.select("table tr"):
    cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
    rows.append(cells)
```

**Extract all images:**

```python
for img in soup.find_all("img"):
    print(img.get("src"), img.get("alt"))
```

**Safe extraction (avoid crashes on missing elements):**

```python
el = soup.select_one("span.price")
price = el.get_text(strip=True) if el else None
```

**Remove scripts and styles before extracting text:**

```python
for t in soup(["script", "style"]):   # calling soup(...) is shorthand for find_all
    t.decompose()
text = soup.get_text(" ", strip=True)
```

## Quick reference

| Task | Command |
|---|---|
| Parse HTML | `BeautifulSoup(html, "html.parser")` |
| First matching tag | `soup.find("tag")` / `soup.select_one("css")` |
| All matching tags | `soup.find_all("tag")` / `soup.select("css")` |
| Attribute value | `tag.get("attr")` or `tag["attr"]` |
| Text content | `tag.get_text(strip=True)` |
| Children / parent | `tag.children` / `tag.parent` |
| Next / previous sibling | `tag.find_next_sibling()` / `tag.find_previous_sibling()` |
| Pretty print | `soup.prettify()` |
| Remove a tag | `tag.decompose()` |

## Tips

- BeautifulSoup only parses HTML. It doesn't fetch pages, so pair it with `requests` or `httpx`.
- It won't run JavaScript. If the content you want loads dynamically, you'll need something like Selenium or Playwright, or the site's underlying API.
- Check a site's `robots.txt` and terms of service before scraping, and add delays between requests.
