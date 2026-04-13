import streamlit as st
import requests
import json
import os

API_URL = "https://www.googleapis.com/books/v1/volumes"
API_KEY = "AIzaSyDo6Brcnd5HhmEluXO9qxOj-rkgtMTYSSo"
SAVE_FILE = "saved_books.json"


# -------------------------
# Load saved books
# -------------------------
def load_saved_books():
    if not os.path.exists(SAVE_FILE):
        return []

    with open(SAVE_FILE, "r") as f:
        return json.load(f)


# -------------------------
# Save book
# -------------------------
def save_book(book):

    books = load_saved_books()

    if book not in books:
        books.append(book)

    with open(SAVE_FILE, "w") as f:
        json.dump(books, f, indent=4)


# -------------------------
# Search books
# -------------------------
def search_books(query):

    if not query:
        return []

    params = {
        "q": query,
        "maxResults": 10,
        "key": API_KEY
    }

    response = requests.get(API_URL, params=params)

    data = response.json()

    return data.get("items", [])


# -------------------------
# UI
# -------------------------
st.set_page_config(page_title="Book Saver", layout="wide")

st.title("📚 Book Saver")

menu = st.sidebar.selectbox(
    "Menu",
    ["Search Books", "Saved Books"]
)

# -------------------------
# SEARCH PAGE
# -------------------------
if menu == "Search Books":

    st.subheader("Search for books")

    query = st.text_input("Type a book name (search starts automatically)")

    results = search_books(query)

    if results:

        for i, item in enumerate(results):

            info = item["volumeInfo"]

            title = info.get("title", "No title")
            authors = info.get("authors", [])
            description = info.get("description", "")

            cover = None
            if "imageLinks" in info:
                cover = info["imageLinks"].get("thumbnail")

            col1, col2 = st.columns([1,4])

            with col1:
                if cover:
                    st.image(cover)

            with col2:

                st.subheader(title)

                if authors:
                    st.write("Author:", ", ".join(authors))

                if description:
                    st.write(description[:250] + "...")

                book = {
                    "title": title,
                    "authors": authors,
                    "description": description,
                    "cover": cover
                }

                if st.button("💾 Save Book", key=f"save_{item['id']}"):
                    save_book(book)
                    st.success("Book saved!")

            st.divider()

# -------------------------
# SAVED BOOKS PAGE
# -------------------------
if menu == "Saved Books":

    st.subheader("Your Saved Books")

    books = load_saved_books()

    if books:

        for book in books:

            col1, col2 = st.columns([1,4])

            with col1:
                if book["cover"]:
                    st.image(book["cover"])

            with col2:
                st.subheader(book["title"])

                if book["authors"]:
                    st.write("Author:", ", ".join(book["authors"]))

                if book["description"]:
                    st.write(book["description"][:250] + "...")

            st.divider()

    else:
        st.info("No saved books yet.")