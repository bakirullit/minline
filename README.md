# Minline

[![PyPI version](https://badge.fury.io/py/minline.svg)](https://pypi.org/project/minline/)
[![License: CUSTOM](https://img.shields.io/badge/License-Custom-green.svg)](./LICENSE)
[![Build](https://github.com/bakirullit/minline/actions/workflows/workflow.yml/badge.svg)](https://github.com/bakirullit/minline/actions)

**Minline** is a lightweight, modular framework built on top of **Aiogram 3.x** for rapidly developing Telegram bots with structured menu navigation, components, and routing mechanics.

## ✨ Features

- 📦 Clean `@app.menu("path")` routing system
- 🔁 Automatic back button support with path trimming (`#route://`)
- 🧩 Easy-to-extend components (e.g., Button, Menu)
- ⚙️ Supports dynamic menu updates and custom actions
- 🪶 Lightweight and dependency-minimal

## 🚀 Installation

```bash
pip install minline
```

## 🧪 Quick Example

```python
from minline import MinlineApp, Menu, Button

app = MinlineApp("YOUR_BOT_TOKEN")

@app.menu("main")
def main_menu():
    return Menu(
        menu_id="main",
        controls=[
            [Button("Go to Settings", "#route://settings")],
            [Button("Profile", "open_profile")]
        ]
    )

@app.menu("main/settings")
def settings_menu():
    return Menu(
        menu_id="settings",
        controls=[
            [Button("Notifications", "toggle_notifications")]
        ]
    )

app.run()
```

## 📚 Documentation

Coming soon at: [https://bakirullit.github.io/minline](https://bakirullit.github.io/minline)

Until then, check the `examples/` folder or open an issue.

## 🛠️ Developing Locally

```bash
git clone https://github.com/bakirullit/minline.git
cd minline
poetry install  # or pip install -e .
```

## 🗂️ Project Structure

```
minline/
├── __init__.py
├── app.py
├── menu.py
├── button.py
├── ...
```

## 🧪 Tests

> Coming soon. Contributions are welcome.

## 📦 Publishing (for Maintainers)

Releases are handled via [Trusted Publishing](https://docs.pypi.org/trusted-publishers/):

```bash
git tag v0.x.x
git push origin v0.x.x
```

CI/CD will automatically build and publish to PyPI.

## 📝 License

Custom License — see [`LICENSE`](./LICENSE)

---

Built with ❤️ by [@bakirullit](https://github.com/bakirullit)