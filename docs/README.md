# Vantage CLI

**Vantage** is a lightweight, modular command-line interface tool designed for fast IP network data retrieval and geolocation analysis directly from your terminal.

---

## 🚀 Features

- **Dynamic Querying**: Fetch geolocation details for any public IP address or analyze your current network connection automatically.
- **Terminal Visual Dashboard**: Clean, emoji-enhanced visual breakdown of core network attributes.
- **Robust Error Handling**: Gracefully fallback on missing parameters or unmapped provider fields.

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Standard Local / Editable Install
Clone the repository and install the package locally using `pip`:

```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/vantage.git](https://github.com/yourusername/vantage.git)
cd vantage

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# 3. Install in editable mode
pip install -e .
```

---

## 💻 Detailed Usage Guide

Once installed via `setup.py`, the CLI registers the executable global command `vantage`. You can also run the tool directly via Python scripts during development.

### 1. Check Your Own Public Network
Running the command without any flags automatically fetches your current public IP address and network provider info:

```bash
# Global CLI command
vantage

# Alternative (Development mode)
python main.py
```

### 2. Query a Specific IP Address
Pass any valid public IPv4 address using the `-i` or `--ip` flag:

```bash
# Short flag
vantage -i 8.8.8.8

# Long flag
vantage --ip 1.1.1.1

# Alternative (Development mode)
python main.py -i 8.8.8.8
```

### 3. Display Help & Command Line Options
To view available arguments and usage instructions directly in your terminal:

```bash
vantage --help
```

---

## 📊 Sample Visual Dashboard Output

When querying a target IP (e.g., `8.8.8.8`), Vantage processes null or missing fields gracefully into visual indicators:

```text
 IP Address  : 8.8.8.8
🗺️  Location    : Unknown, US (NA)
📮 Postal Code : N/A
📍 Coordinates : 37.751, -97.822
🏢 Provider    : Google LLC
```

---

## 🧱 Project Architecture

Vantage adheres to strict separation of concerns across a modular architecture:

- `main.py`: Core entry point wiring CLI arguments to data operations.
- `cli.py`: User interface, argument parsing (`argparse`), and terminal dashboard layout.
- `api.py`: External network data fetching layer with error handling.
- `setup.py`: Packaging entry point configuring global command registration.

---

## 🤝 Contributing

We follow [Conventional Commits](https://www.conventionalcommits.org/) for clean Git history. Please format your commit messages accordingly (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`).