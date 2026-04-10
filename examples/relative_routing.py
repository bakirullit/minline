#!/usr/bin/env python3
"""
Relative routing example for Minline.

Demonstrates:
- Relative routes (#route:path) vs absolute (#route:/path)
- How relative routes append to current path
- Navigation hierarchy without hardcoding paths

Key concept:
  Current path: /catalog/books/fiction
  #route:reviews  -> /catalog/books/fiction/reviews
  #route:/        -> / (absolute, always goes to root)
"""

from minline import MinlineApp, Menu, Button

app = MinlineApp("BOT_TOKEN")


@app.route("/")
def root():
    return Menu(
        menu_id="root",
        text="📚 Catalog",
        controls=[
            [Button("📖 Books", "#route:books")],  # Relative: /books
            [Button("📰 Magazines", "#route:magazines")]  # Relative: /magazines
        ]
    )


@app.route("/books")
def books():
    return Menu(
        menu_id="books",
        text="📖 Books",
        controls=[
            [Button("🔖 Fiction", "#route:fiction")],  # Relative: /books/fiction
            [Button("📚 Non-Fiction", "#route:nonfiction")]  # Relative: /books/nonfiction
        ]
    )


@app.route("/books/fiction")
def fiction():
    return Menu(
        menu_id="fiction",
        text="🔖 Fiction Books",
        controls=[
            [Button("📝 Add Review", "#route:reviews")],  # Relative: /books/fiction/reviews
            [Button("⭐ Top Rated", "#route:top")]  # Relative: /books/fiction/top
        ]
    )


@app.route("/books/fiction/reviews")
def fiction_reviews():
    return Menu(
        menu_id="reviews",
        text="📝 Write a Review",
        controls=[]
    )


@app.route("/books/fiction/top")
def fiction_top():
    return Menu(
        menu_id="top",
        text="⭐ Top Rated Fiction",
        controls=[
            [Button("1. The Great Gatsby", "#route:/")],
            [Button("2. 1984", "#route:/")],
            [Button("3. To Kill a Mockingbird", "#route:/")]
        ]
    )


@app.route("/books/nonfiction")
def nonfiction():
    return Menu(
        menu_id="nonfiction",
        text="📚 Non-Fiction Books",
        controls=[
            [Button("🎯 Top Rated", "#route:top")],  # Relative: /books/nonfiction/top
            [Button("📊 By Category", "#route:category")]  # Relative: /books/nonfiction/category
        ]
    )


@app.route("/books/nonfiction/top")
def nonfiction_top():
    return Menu(
        menu_id="nonfiction_top",
        text="⭐ Top Non-Fiction",
        controls=[]
    )


@app.route("/books/nonfiction/category")
def nonfiction_category():
    return Menu(
        menu_id="category",
        text="📊 Categories",
        controls=[
            [Button("🌍 History", "#route:history")],
            [Button("🔬 Science", "#route:science")]
        ]
    )


@app.route("/books/nonfiction/category/history")
def history():
    return Menu(
        menu_id="history",
        text="🌍 History Books",
        controls=[]
    )


@app.route("/books/nonfiction/category/science")
def science():
    return Menu(
        menu_id="science",
        text="🔬 Science Books",
        controls=[]
    )


@app.route("/magazines")
def magazines():
    return Menu(
        menu_id="magazines",
        text="📰 Magazines",
        controls=[
            [Button("🎮 Tech", "#route:tech")],  # Relative: /magazines/tech
            [Button("💼 Business", "#route:business")]  # Relative: /magazines/business
        ]
    )


@app.route("/magazines/tech")
def tech_magazines():
    return Menu(
        menu_id="tech",
        text="🎮 Tech Magazines",
        controls=[]
    )


@app.route("/magazines/business")
def business_magazines():
    return Menu(
        menu_id="business",
        text="💼 Business Magazines",
        controls=[]
    )


if __name__ == "__main__":
    app.run()
