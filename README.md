# Static Website Builder

This project is a Python-powered static site generator that turns Markdown content into a publishable website. It cleans and rebuilds the `docs/` directory, copies static assets, translates Markdown into HTML using a custom parser, and applies a shared HTML template so the output is ready for GitHub Pages or any static host.

## Highlights
- Processes every Markdown file in `content/` (recursively) and renders matching HTML pages in `docs/`.
- Copies everything from `static/` into `docs/` so stylesheets and images stay in sync with the generated pages.
- Supports headings, paragraphs, bold/italic/code spans, images, links, blockquotes, and ordered/unordered lists via the Markdown parser in `src/`.
- Provides simple shell entry points: `build.sh` for production builds with a configurable base path, and `main.sh` for local preview with Python's built-in web server.
- Ships with unit tests in `src/tests/` to pin down the Markdown parsing and HTML rendering logic.

## How It Works
1. **Entry point (`src/main.py`)** – Accepts an optional base URL, clears the existing `docs/` output (`clean_public`), copies static assets (`copy_to_public`), and walks the `content/` tree to rebuild each page with `generate_pages_recursive`.
2. **Markdown parsing (`src/helpers.py`, `src/blocks.py`)** – Splits Markdown into blocks, determines each block's type (heading, list, quote, code, etc.), and converts inline syntax into `TextNode` objects. These nodes become HTML through small `HTMLNode` wrappers.
3. **Templating (`template.html`)** – Each rendered page injects its title (`{{ Title }}`) and body (`{{ Content }}`) into a shared template. Links and image sources are rewritten when a non-root base path is supplied so the site works when hosted in a subdirectory.
4. **Assets (`static/`)** – Static files (CSS, images) are copied as-is, keeping design and media alongside generated HTML.
5. **Output (`docs/`)** – Contains the finished site, ready to serve locally or publish.

## Project Layout
- `content/` – Source Markdown for the homepage, contact page, and nested blog posts.
- `docs/` – Generated website (tracked here for quick inspection or deployment).
- `src/` – Python package with the Markdown parser, HTML node models, and build orchestration code.
- `static/` – Stylesheet and shared images copied verbatim into `docs/`.
- `template.html` – Base HTML shell used for every generated page.
- `build.sh`, `main.sh`, `test.sh` – Helper scripts for building, serving, and testing.

## Usage
- **Generate the site**: `./build.sh` (assumes Python 3.10+ and installs are already available). The script sets the base path to `/static_website_builder/`, which is useful when deploying to GitHub Pages under that subdirectory.
- **Preview locally**: `./main.sh` runs the generator and then serves `docs/` at http://localhost:8888 via `python3 -m http.server`.
- **Run tests**: `./test.sh` executes the unit suite (`python3 -m unittest discover -s src/tests`).

## Extending the Site
- Add new Markdown files anywhere under `content/`; the same directory structure will be reproduced in `docs/` with `.html` outputs.
- Customize presentation by editing `template.html` or adjusting styles in `static/index.css`.
- Update or add images in `static/images/`; refer to them in Markdown with standard image syntax (`![alt](path)`), and they will be copied automatically.

## Markdown Features Supported
- Headings (`#` through `######`)
- Paragraphs and line breaks
- Bold (`**text**`), italic (`_text_`), and inline code (`` `code` ``)
- Links (`[label](url)`) and images (`![alt](url)`)
- Blockquotes (`> quote`)
- Ordered (`1.`) and unordered (`-`) lists
- Fenced code blocks ( ``` ) rendered inside `<pre><code>`

## LIVE Preview
- [Static Website Generator from .md](https://vladutmocanugabriel.github.io/static_website_builder/)

Together, these pieces form a minimal yet full-featured static site pipeline that you can adapt for new content, custom designs, or deployment targets.
