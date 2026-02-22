# 🤝 Contributing to Network Sniffer Pro

We welcome contributions from the community! Whether you're fixing a bug, adding a feature, or improving documentation, your help is appreciated.

## 🛠️ Developer Setup

To get started with development, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ssneon1/Network-Sniffer-Pro.git
   cd Network-Sniffer-Pro
   ```

2. **Install Npcap:**
   Download and install the Npcap SDK from [npcap.com](https://npcap.com). Make sure to enable "WinPcap API-compatible Mode".

3. **Set up a Python Virtual Environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

4. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run the App:**
   ```powershell
   python main.py
   ```

## 📜 Pull Request Process

1. **Fork the repo** and create your branch from `main`.
2. **If you've added code** that should be tested, add tests.
3. **Ensure the code lints** and follows the existing style.
4. **Update the documentation** if you're introducing a change in behavior or features.
5. **Issue a Pull Request** with a clear description of the problem and your solution.

## 🎨 Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Use meaningful variable and function names.
- Keep functions focused and concise.
- Add comments for complex logic.

## 🐛 Reporting Bugs

Use the GitHub Issues tracker to report bugs. Please include:
- A clear summary of the issue.
- Steps to reproduce.
- Expected vs. Actual behavior.
- Screenshots if applicable.
