# import streamlit as st
# import requests
# import json
# import os

# API_KEY = st.secrets["api_key"]
# API_URL = st.secrets["api_url"]
# SAVE_FILE = "saved_books.json"


# # -------------------------
# # Load saved books
# # -------------------------
# def load_saved_books():
#     if not os.path.exists(SAVE_FILE):
#         return []

#     with open(SAVE_FILE, "r") as f:
#         return json.load(f)


# # -------------------------
# # Save book
# # -------------------------
# def save_book(book):

#     books = load_saved_books()

#     if book not in books:
#         books.append(book)

#     with open(SAVE_FILE, "w") as f:
#         json.dump(books, f, indent=4)


# # -------------------------
# # Search books
# # -------------------------
# def search_books(query):

#     if not query:
#         return []

#     params = {
#         "q": query,
#         "maxResults": 10,
#         "key": API_KEY
#     }

#     response = requests.get(API_URL, params=params)

#     data = response.json()

#     return data.get("items", [])


# # -------------------------
# # UI
# # -------------------------
# st.set_page_config(page_title="Book Saver", layout="wide")

# st.title("📚 Book Saver")

# menu = st.sidebar.selectbox(
#     "Menu",
#     ["Search Books", "Saved Books"]
# )

# # -------------------------
# # SEARCH PAGE
# # -------------------------
# if menu == "Search Books":

#     st.subheader("Search for books")

#     query = st.text_input("Type a book name (search starts automatically)")

#     results = search_books(query)

#     if results:

#         for i, item in enumerate(results):

#             info = item["volumeInfo"]

#             title = info.get("title", "No title")
#             authors = info.get("authors", [])
#             description = info.get("description", "")

#             cover = None
#             if "imageLinks" in info:
#                 cover = info["imageLinks"].get("thumbnail")

#             col1, col2 = st.columns([1,4])

#             with col1:
#                 if cover:
#                     st.image(cover)

#             with col2:

#                 st.subheader(title)

#                 if authors:
#                     st.write("Author:", ", ".join(authors))

#                 if description:
#                     st.write(description[:250] + "...")

#                 book = {
#                     "title": title,
#                     "authors": authors,
#                     "description": description,
#                     "cover": cover
#                 }

#                 if st.button("💾 Save Book", key=f"save_{item['id']}"):
#                     save_book(book)
#                     st.success("Book saved!")

#             st.divider()

# # -------------------------
# # SAVED BOOKS PAGE
# # -------------------------
# if menu == "Saved Books":

#     st.subheader("Your Saved Books")

#     books = load_saved_books()

#     if books:

#         for book in books:

#             col1, col2 = st.columns([1,4])

#             with col1:
#                 if book["cover"]:
#                     st.image(book["cover"])

#             with col2:
#                 st.subheader(book["title"])

#                 if book["authors"]:
#                     st.write("Author:", ", ".join(book["authors"]))

#                 if book["description"]:
#                     st.write(book["description"][:250] + "...")

#------


import streamlit as st
import requests
import json
import os

# -------------------------
# CONFIGURATION
# -------------------------
# Use hardcoded URL - no need for secret
API_URL = "https://www.googleapis.com/books/v1/volumes"

# Get API key from secrets with error handling
try:
    API_KEY = st.secrets["api_key"]
except KeyError:
    st.error("⚠️ API key not found! Please add 'api_key' to Streamlit secrets.")
    st.stop()

SAVE_FILE = "saved_books.json"

# -------------------------
# Load saved books
# -------------------------
def load_saved_books():
    """Load saved books from JSON file"""
    if not os.path.exists(SAVE_FILE):
        return []
    
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

# -------------------------
# Save book
# -------------------------
def save_book(book):
    """Save a book to JSON file"""
    books = load_saved_books()
    
    # Check if book already exists (by title)
    if not any(b["title"] == book["title"] for b in books):
        books.append(book)
        
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(books, f, indent=4)
            return True
        except IOError:
            return False
    return False

# -------------------------
# Search books with error handling
# -------------------------
def search_books(query):
    """Search Google Books API with error handling"""
    if not query:
        return []
    
    params = {
        "q": query,
        "maxResults": 10,
        "key": API_KEY
    }
    
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        data = response.json()
        return data.get("items", [])
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Error: {str(e)}")
        return []
    except json.JSONDecodeError:
        st.error("❌ Invalid response from API")
        return []

# -------------------------
# UI
# -------------------------
st.set_page_config(page_title="Book Saver", layout="wide")

st.title("📚 Book Saver")

# Warning about cloud storage limitations
st.info("💡 **Note:** Saved books are stored locally and will disappear when the app restarts. For permanent storage, consider using a database like SQLite or Firebase.")

menu = st.sidebar.selectbox(
    "Menu",
    ["Search Books", "Saved Books"]
)

# -------------------------
# SEARCH PAGE
# -------------------------
if menu == "Search Books":
    st.subheader("🔍 Search for books")
    
    query = st.text_input("Type a book name (search starts automatically)")
    
    if query:
        with st.spinner("Searching..."):
            results = search_books(query)
        
        if results:
            st.success(f"Found {len(results)} books")
            
            for i, item in enumerate(results):
                info = item["volumeInfo"]
                
                title = info.get("title", "No title")
                authors = info.get("authors", [])
                description = info.get("description", "")
                
                cover = None
                if "imageLinks" in info:
                    cover = info["imageLinks"].get("thumbnail")
                
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    if cover:
                        st.image(cover, width=120)
                    else:
                        st.write("📖")
                
                with col2:
                    st.subheader(title)
                    
                    if authors:
                        st.write("**Author:**", ", ".join(authors))
                    
                    if description:
                        st.write(description[:250] + "...")
                    
                    book = {
                        "title": title,
                        "authors": authors,
                        "description": description,
                        "cover": cover
                    }
                    
                    if st.button("💾 Save Book", key=f"save_{item['id']}"):
                        if save_book(book):
                            st.success(f"✅ '{title}' saved!")
                        else:
                            st.warning("⚠️ Book already saved or save failed")
                
                st.divider()
        elif query:
            st.warning("No books found. Try a different search term.")

# -------------------------
# SAVED BOOKS PAGE
# -------------------------
elif menu == "Saved Books":
    st.subheader("📚 Your Saved Books")
    
    books = load_saved_books()
    
    if books:
        st.write(f"You have **{len(books)}** saved books")
        
        # Add a clear all button
        if st.button("🗑️ Clear All Saved Books"):
            try:
                with open(SAVE_FILE, "w") as f:
                    json.dump([], f)
                st.success("All books cleared!")
                st.rerun()
            except IOError:
                st.error("Failed to clear books")
        
        for book in books:
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if book.get("cover"):
                    st.image(book["cover"], width=120)
                else:
                    st.write("📖")
            
            with col2:
                st.subheader(book.get("title", "No title"))
                
                if book.get("authors"):
                    st.write("**Author:**", ", ".join(book["authors"]))
                
                if book.get("description"):
                    st.write(book["description"][:250] + "...")
            
            st.divider()
    else:
        st.info("No saved books yet. Go to 'Search Books' to add some!")

# -------------------------
# SIDEBAR INFO
# -------------------------
st.sidebar.markdown("---")
st.sidebar.info(
    "**About:**\n"
    "- Search books using Google Books API\n"
    "- Save your favorites\n"
    "- ⚠️ Books are saved locally and will reset when the app restarts"
)

#             st.divider()

#     else:
#         st.info("No saved books yet.")
