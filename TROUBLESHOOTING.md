# ⚠️ Troubleshooting: Network Sniffer Pro

If you're encountering issues while running or installing Network Sniffer Pro, check the common solutions below.

## 🛜 Packet Capture Issues

### "No Interface Found" or "Default Interface Only"
- **Cause:** Npcap is not installed or the driver is not running.
- **Solution:** 
  1. Ensure you installed `npcap-installer.exe` (provided in the `dist` folder).
  2. During Npcap installation, make sure to check "Install Npcap in WinPcap API-compatible Mode".
  3. Restart your computer if the interfaces still don't show up.

### Permission Denied (Admin Required)
- **Cause:** Capturing network traffic requires administrative privileges on Windows.
- **Solution:** Right-click `main.exe` (or your IDE) and select **Run as Administrator**.

### No Packets Captured (Capture is running but list is empty)
- **Cause:** Incorrect interface selected or firewall/antivirus blocking the sniffer.
- **Solution:**
  1. Try selecting a different interface from the dropdown menu (e.g., your specific Wi-Fi card instead of "Default").
  2. Temporarily disable your firewall or whitelist the application.

## 🌐 Web Dashboard Issues

### Page "Cannot be Displayed" at localhost:5000
- **Cause:** The Flask server failed to start or port 5000 is occupied.
- **Solution:**
  1. Check the terminal/console for error messages like `OSError: [Errno 98] Address already in use`.
  2. If port 5000 is occupied, you might need to change the port in `main.py` (`app.run(port=5000)`).
  3. Ensure no other application (like AirPlay on macOS or another dev server) is using port 5000.

### Dashboard is blank or not updating
- **Cause:** WebSocket connection failed.
- **Solution:**
  1. Hard refresh the browser (`Ctrl + F5`).
  2. Ensure you are using a modern browser (Chrome, Firefox, Edge).

## 🛠️ Builder/Developer Issues

### PyInstaller Build Fails
- **Cause:** Missing dependencies or incorrect `_MEIPASS` handling.
- **Solution:**
  1. Run `pip install -r requirements.txt` before building.
  2. Ensure you are using the provided `main.spec` file.

### "Module Not Found: scapy"
- **Solution:** Make sure you are running in the correct virtual environment. 
  ```powershell
  .\.venv\Scripts\activate
  pip install scapy
  ```
