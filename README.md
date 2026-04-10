# Minline

Minline is a lightweight navigation-first framework built on top of **aiogram 3.x** for creating Telegram bots with **structured menus**, **relative routing**, and **stateful navigation**.

It is designed for developers who want:
- deterministic menu routing
- zero magic strings scattered across handlers
- scalable menu hierarchies
- predictable back navigation

Minline treats bot UI as a **routing problem**, not a callback mess.

---

## Creating Menus

`Menu` takes three parameters:

```python
Menu(
    menu_id="settings",      # Unique identifier for this menu
    controls=[               # Button layout
        [Button("Save", "#route:/save")],
        [Button("Reset", "#route:/reset")]
    ],
    text="⚙️ Settings",      # Text shown to user (default: menu_id)
    back=True                # Show back button (default: True)
)
```

**Important**: `text` is what users see. `menu_id` is an internal identifier.

---

## Core Concepts

### 1. Routes

Routes are hierarchical paths, similar to URLs:

```

/
└── settings
└── books

````

Each route maps to a function returning a `Menu`.

```python
@app.route("/settings/books")
def books():
    ...
````

---

### 2. Navigation Protocol

Minline defines a strict navigation protocol:

| Action         | Syntax             | Meaning                |
| -------------- | ------------------ | ---------------------- |
| Absolute route | `#route:/settings` | Jump to exact path     |
| Relative route | `#route:books`     | Append to current path |
| Back           | `#route://`        | Go to previous path    |

These constants are centralized in `NavigationProtocol`.

---

### 3. Relative Routing

If current route is:

```
/settings
```

Then:

```python
Button("Books", "#route:books")
```

Resolves to:

```
/settings/books
```

No manual string concatenation. No guessing.

---

### 4. Automatic Back Button

Menus automatically receive a **Back** button when:

* route is not `/`
* `auto_back=True` (default)

You can disable it per menu.

---

### 5. 404 Handling

Unknown routes do not crash the bot.

Instead:

* previous route is preserved
* user sees a Not Found menu
* Back always returns safely

---

---

## Installation

```bash
pip install minline
```

Or from source:

```bash
git clone https://github.com/bakirullit/minline
cd minline
pip install -e .
```

**Requirements**:
- Python ≥ 3.10
- aiogram ≥ 3.0
- aiosqlite ≥ 0.17

---

## Configuration

### Custom Session Manager

By default, Minline uses SQLite for session storage. You can provide your own:

```python
from minline import MinlineApp
from minline.session import SqliteSessionManager

app = MinlineApp(
    token="BOT_TOKEN",
    session_manager=SqliteSessionManager("sessions.db")
)
```

### Navigation Stack TTL

Clean up old user stacks automatically (default: 24 hours):

```python
from minline.routing import NavigationStack

nav = NavigationStack(ttl_seconds=86400)  # 24 hours
```

---

## Minimal Example

```python
from minline import MinlineApp, Menu, Button

app = MinlineApp("BOT_TOKEN")

@app.route("/")
def main():
    return Menu(
        menu_id="main",
        controls=[
            [Button("Settings", "#route:/settings")]
        ]
    )

@app.route("/settings")
def settings():
    return Menu(
        menu_id="settings",
        controls=[
            [Button("Books", "#route:books")]
        ]
    )

@app.route("/settings/books")
def books():
    return Menu(
        menu_id="books",
        controls=[]
    )

app.run()
```

---

## Design Philosophy

* Navigation is **data**, not callbacks
* Routing is **explicit**
* Back behavior is **deterministic**
* Menus are **pure objects**
* aiogram is infrastructure, not architecture

Minline does not fight Telegram.
It just refuses to pretend callbacks are a routing system.

---

## Status

This project is under active development.
Recent improvements (April 2026):

- **✅ AsyncIO-safe sessions**: Replaced `JsonSessionManager` with `SqliteSessionManager` using `asyncio.Lock`
- **✅ Memory cleanup**: `NavigationStack` now includes automatic TTL-based cleanup (24h default)
- **✅ Proper message editing**: Callback messages are edited in-place, no deletion/resend spam
- **✅ Better error logging**: Replaced silent `except: pass` with structured logging (debug/warning/error)
- **✅ Correct text rendering**: Menus now display `menu.text` instead of `menu_id`

APIs are stable. All core features work as intended.
