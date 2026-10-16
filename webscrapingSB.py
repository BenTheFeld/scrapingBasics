from bs4 import BeautifulSoup 
import requests
import csv

url = "https://books.toscrape.com/"
response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
books = soup.find_all("ul", class_="nav nav-list")

with open("books.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Category"])

for book in books[0].select("ul ul a"):
    category = book.string
    print(category)
    #writer.writerow([category])

print(books)