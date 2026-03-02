# 🔌 API & Communication Reference: Network Sniffer Pro

Network Sniffer Pro uses a combination of Flask routes for static content and SocketIO for real-time packet streaming.

## 📡 SocketIO Events

The application emits events to the dashboard using the `flask-socketio` library.

### `new_packet` (Server -> Client)
Triggered whenever a new packet is captured and passes the filters.

**Payload Structure:**
```json
{
  "time": "14:20:05.123",        // Timestamp
  "src": "192.168.1.10",         // Source IP
  "dst": "8.8.8.8",              // Destination IP
  "proto": "TCP",                // Protocol (TCP, UDP, ICMP, HTTP, etc.)
  "size": 64,                    // Packet size in bytes
  "info": "Flags: PA | Port: 80", // Human-readable summary
  "security": "Clean",           // Security status (Clean or Alert)
  "is_alert": false,             // Boolean indicating a security warning
  "details": "..."               // Full hex dump and layer analysis (string)
}
```

## 🌐 Flask Routes

### `GET /`
Serves the main web dashboard interface (`templates/index.html`).

## 🛠️ Internal Filtering Logic

### Protocol Flags
The sniffer identifies protocols based on both IP headers and common port numbers:
- **TCP (6)**, **UDP (17)**, **ICMP (1)**.
- **HTTP**: Identified if Port is `80`.
- **HTTPS**: Identified if Port is `443` (Payload is not decrypted).

### Credential Scanning
The `check_for_credentials` function scans the `Raw` layer of packets for the following keywords:
`user`, `pass`, `login`, `email`, `secret`, `token`, `pwd`.

> [!NOTE]
> Credential scanning is only performed on non-HTTPS traffic as the contents of HTTPS traffic are encrypted.

## 🧱 Data Structures

### `packet_map` (Python Dictionary)
Used in the native UI to store `Scapy` packet objects indexed by their `Treeview` ID. This allows the application to retrieve and show full details when a user clicks on a packet in the list.

### `target_ips` (List)
Stores the resolved IP addresses of the target domain/host specified by the user for precision filtering.
