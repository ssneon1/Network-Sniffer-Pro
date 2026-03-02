import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os
import sys
import threading
import socket
from datetime import datetime
from scapy.all import sniff, IP, IPv6, TCP, UDP, ICMP, Ether, conf, get_if_list, Raw
from flask import Flask, render_template
from flask_socketio import SocketIO

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Flask App Setup
template_dir = resource_path('templates')
app_flask = Flask(__name__, template_folder=template_dir)
socketio = SocketIO(app_flask, async_mode='threading')

@app_flask.route('/')
def index():
    return render_template('index.html')

class NetworkSnifferApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Network Sniffer Pro")
        self.geometry("1100x900")
        
        # Set appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Variables
        self.is_capturing = False
        self.packet_map = {} 
        self.packet_counter = 0
        self.capture_thread = None
        self.target_ip = None

        self.setup_ui()
        self.apply_treeview_style()
        self.start_web_server()
        
        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.is_capturing = False
        try:
            self.destroy()
        except:
            pass
        os._exit(0)

    def start_web_server(self):
        def run_flask():
            socketio.run(app_flask, port=5000, host='0.0.0.0', log_output=False)
        
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

    def apply_treeview_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="white", 
                        fieldbackground="#2b2b2b", 
                        borderwidth=0,
                        rowheight=25)
        style.map("Treeview", background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", 
                        background="#333333", 
                        foreground="white", 
                        relief="flat")
        style.map("Treeview.Heading", background=[('active', '#404040')])

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="SNIFFER PRO", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        self.start_btn = ctk.CTkButton(self.sidebar, text="Start Capture", command=self.toggle_capture, fg_color="green", hover_color="darkgreen")
        self.start_btn.pack(pady=10, padx=20)

        self.clear_btn = ctk.CTkButton(self.sidebar, text="Clear Data", command=self.clear_capture)
        self.clear_btn.pack(pady=10, padx=20)

        # Interface Selector
        self.iface_label = ctk.CTkLabel(self.sidebar, text="Select Interface:")
        self.iface_label.pack(pady=(20, 5))
        
        try:
            interfaces = [str(i.name) for i in get_if_list()]
            if not interfaces: interfaces = ["Default"]
        except:
            interfaces = ["Default"]
            
        self.iface_var = ctk.StringVar(value=interfaces[0])
        self.iface_menu = ctk.CTkOptionMenu(self.sidebar, values=interfaces, variable=self.iface_var)
        self.iface_menu.pack(pady=5, padx=20)

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: IDLE", text_color="gray")
        self.status_label.pack(pady=10)

        # Targeting UI
        self.target_label = ctk.CTkLabel(self.sidebar, text="Target Site (Domain/IP):")
        self.target_label.pack(pady=(20, 5))
        self.target_entry = ctk.CTkEntry(self.sidebar, placeholder_text="e.g. google.com")
        self.target_entry.pack(pady=5, padx=20)

        self.protocol_label = ctk.CTkLabel(self.sidebar, text="Protocol Filter:")
        self.protocol_label.pack(pady=(20, 5))
        self.protocol_var = ctk.StringVar(value="All")
        self.protocol_menu = ctk.CTkOptionMenu(self.sidebar, values=["All", "TCP", "UDP", "ICMP", "HTTP", "HTTPS"], variable=self.protocol_var)
        self.protocol_menu.pack(pady=10, padx=20)

        # Docs Button
        self.docs_btn = ctk.CTkButton(self.sidebar, text="📖 Open Documentation", 
                                     command=self.open_docs, 
                                     fg_color="transparent", border_width=1)
        self.docs_btn.pack(pady=20, padx=20)

        self.web_info = ctk.CTkLabel(self.sidebar, text="Web View: http://localhost:5000", font=ctk.CTkFont(size=10), text_color="gray")
        self.web_info.pack(side="bottom", pady=20)

        # Main Content
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=3)
        self.main_frame.grid_rowconfigure(1, weight=2)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.list_container = ctk.CTkFrame(self.main_frame)
        self.list_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        columns = ("Time", "Source", "Destination", "Protocol", "Length", "Info", "Security")
        self.tree = ttk.Treeview(self.list_container, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.column("Time", width=120)
        self.tree.column("Info", width=200)
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_packet_select)

        self.scrollbar = ttk.Scrollbar(self.list_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.details_box = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(family="Consolas", size=11))
        self.details_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.details_box.insert("0.0", "Capture packets to see detailed hex/layer data...")
        self.details_box.configure(state="disabled")

    def open_docs(self):
        import webbrowser
        webbrowser.open("http://localhost:5000") # Points to the dashboard for now as live docs

    def toggle_capture(self):
        if not self.is_capturing:
            target = self.target_entry.get().strip()
            self.target_ips = []
            if target:
                try:
                    # Resolve all possible IPs for the domain
                    addr_info = socket.getaddrinfo(target, None)
                    self.target_ips = list(set([info[4][0] for info in addr_info]))
                    print(f"Targeting IPs: {self.target_ips}")
                    self.status_label.configure(text=f"Target: {target}", text_color="blue")
                except Exception as e:
                    print(f"DNF Resolve Error: {e}")
                    self.target_ips = [target]
                    self.status_label.configure(text=f"Target: {target}", text_color="blue")
            else:
                self.target_ips = []
                self.status_label.configure(text="Capture: GLOBAL", text_color="green")

            self.is_capturing = True
            selected_iface = self.iface_var.get()
            print(f"Starting capture on: {selected_iface}")
            
            self.start_btn.configure(text="Stop Capture", fg_color="red", hover_color="darkred")
            self.capture_thread = threading.Thread(target=self.sniff_packets, daemon=True)
            self.capture_thread.start()
        else:
            self.is_capturing = False
            self.status_label.configure(text="Status: STOPPED", text_color="red")
            self.start_btn.configure(text="Start Capture", fg_color="green", hover_color="darkgreen")

    def check_for_credentials(self, packet):
        if Raw in packet:
            try:
                payload = str(packet[Raw].load).lower()
                keywords = ["user", "pass", "login", "email", "secret", "token", "pwd"]
                found = [k for k in keywords if k in payload]
                if found:
                    return True, f"ALERT: {', '.join(found[:2])}"
            except:
                pass
        return False, "Clean"

    def sniff_packets(self):
        def process_packet(packet):
            if not self.is_capturing: return
            
            proto_name = "OTHER"
            src, dst = "N/A", "N/A"
            security_status = "Clean"
            is_alert = False

            if IP in packet:
                src, dst = packet[IP].src, packet[IP].dst
                proto = packet[IP].proto
                if proto == 6: proto_name = "TCP"
                elif proto == 17: proto_name = "UDP"
                elif proto == 1: proto_name = "ICMP"
            elif IPv6 in packet:
                src, dst = packet[IPv6].src, packet[IPv6].dst
                proto_name = "IPv6"

            if TCP in packet:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80: proto_name = "HTTP"
                elif packet[TCP].dport == 443 or packet[TCP].sport == 443: proto_name = "HTTPS"

            # Site Targeting Logic (Checks both Source and Destination)
            if self.target_ips and src not in self.target_ips and dst not in self.target_ips:
                return

            # Protocol Filter
            f_val = self.protocol_var.get()
            if f_val != "All" and proto_name != f_val: return

            # Credential Scanning (Only for HTTP or plain text protocols)
            if proto_name != "HTTPS":
                is_alert, security_status = self.check_for_credentials(packet)

            # Protocol Specific Info (Educational Data Flow)
            info = ""
            if TCP in packet:
                flags = packet[TCP].flags
                info = f"Flags: {flags} | Port: {packet[TCP].dport}"
            elif UDP in packet:
                info = f"Port: {packet[UDP].dport}"
            elif ICMP in packet:
                info = f"Type: {packet[ICMP].type} (Code: {packet[ICMP].code})"

            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            length = len(packet)
            pkt_summary = (timestamp, src, dst, proto_name, length, info, security_status)
            
            # Send to Browser
            socketio.emit('new_packet', {
                'time': timestamp,
                'src': src,
                'dst': dst,
                'proto': proto_name,
                'size': length,
                'info': info,
                'security': security_status,
                'is_alert': is_alert,
                'details': packet.show(dump=True)
            })

            # Send to Local UI
            self.after(0, lambda: self.add_to_list(pkt_summary, packet, is_alert))

        try:
            selected_iface = self.iface_var.get()
            print(f"Sniffing started on {selected_iface}...")
            if selected_iface != "Default":
                sniff(iface=selected_iface, prn=process_packet, stop_filter=lambda x: not self.is_capturing, store=0)
            else:
                sniff(prn=process_packet, stop_filter=lambda x: not self.is_capturing, store=0)
        except Exception as e:
            print(f"Sniffing Error: {e}")
            self.after(0, lambda: self.show_error(str(e)))

    def add_to_list(self, data, packet, is_alert=False):
        if not hasattr(self, 'tree') or not self.tree.winfo_exists():
            return
        tag = "alert" if is_alert else ""
        iid = self.tree.insert("", "end", values=data, tags=(tag,))
        
        if is_alert:
            self.tree.tag_configure("alert", foreground="orange")

        self.packet_map[iid] = packet
        self.packet_counter += 1
        if self.packet_counter > 500:
            first = self.tree.get_children()[0]
            self.tree.delete(first)
            if first in self.packet_map: del self.packet_map[first]
            self.packet_counter -= 1
        if self.is_capturing: self.tree.see(iid)

    def on_packet_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        pkt = self.packet_map.get(sel[0])
        if pkt:
            self.details_box.configure(state="normal")
            self.details_box.delete("0.0", "end")
            self.details_box.insert("end", pkt.show(dump=True))
            self.details_box.configure(state="disabled")

    def clear_capture(self):
        self.tree.delete(*self.tree.get_children())
        self.packet_map.clear()
        self.packet_counter = 0
        self.details_box.configure(state="normal")
        self.details_box.delete("0.0", "end")
        self.details_box.configure(state="disabled")
        
    def show_error(self, msg):
        print(f"Error: {msg}")

if __name__ == "__main__":
    try:
        app = NetworkSnifferApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
        sys.exit(0)
