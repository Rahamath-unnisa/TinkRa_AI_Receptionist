import customtkinter as ctk
from PIL import Image
from datetime import datetime
import threading

from chatbot import get_response
from speech import speak
from voice_input import listen
from database import get_visitor_count, get_staff_count

# ==========================
# THEME
# ==========================

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class TinkRaApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # --------------------------
        # WINDOW
        # --------------------------
        self.is_speaking = False
        self.title("🤖 TinkRa AI Receptionist")
        self.geometry("1200x700")
        self.minsize(1200, 700)

        # --------------------------
        # GRID
        # --------------------------

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --------------------------
        # BUILD UI
        # --------------------------

        self.create_header()
        self.create_main()
        self.create_bottom()
        self.update_dashboard()  
        # --------------------------
        # START CLOCK
        # --------------------------

        self.update_time()

        # --------------------------
        # WELCOME MESSAGE
        # --------------------------

        self.after(
            1000,
            lambda: self.bot_reply(
                "Hello! Welcome to TinkEdge Robotics Lab. How may I help you today?"
            )
        )
            # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        self.header = ctk.CTkFrame(
            self,
            height=65,
            fg_color="#1565C0",
            corner_radius=0
        )
        self.header.grid(row=0, column=0, sticky="ew")

        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=1)
        self.header.grid_columnconfigure(2, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="🤖 TinkRa AI Receptionist",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.time_label = ctk.CTkLabel(
            self.header,
            text="",
            font=("Segoe UI", 14),
            text_color="white"
        )
        self.time_label.grid(row=0, column=1)

        self.status_top = ctk.CTkLabel(
            self.header,
            text="🟢 Ready",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )
        self.status_top.grid(row=0, column=2, padx=20, sticky="e")



    # =====================================================
    # MAIN AREA
    # =====================================================

    def create_main(self):

        self.main = ctk.CTkFrame(
            self,
            fg_color="#F5F7FA"
        )

        self.main.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # 70 / 30 layout
        self.main.grid_columnconfigure(0, weight=7)
        self.main.grid_columnconfigure(1, weight=3)

        self.main.grid_rowconfigure(0, weight=1)

        self.create_left_panel()
        self.create_right_panel()



    # =====================================================
    # LEFT PANEL
    # =====================================================

    def create_left_panel(self):

        self.left = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=20
        )

        self.left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(20,10),
            pady=20
        )

        # Avatar

        avatar = ctk.CTkImage(
            light_image=Image.open("assets/TinkRah.png"),
            dark_image=Image.open("assets/TinkRah.png"),
            size=(420,420)
        )

        self.avatar = ctk.CTkLabel(
            self.left,
            image=avatar,
            text=""
        )

        self.avatar.pack(pady=(30,15))

        # Status

        self.status_avatar = ctk.CTkLabel(
            self.left,
            text="🟢 Ready",
            font=("Segoe UI",20,"bold"),
            text_color="#2E7D32"
        )

        self.status_avatar.pack(pady=5)

        # Live subtitle

        self.live_text = ctk.CTkLabel(
            self.left,
            text="Welcome to TinkEdge Robotics Lab",
            wraplength=600,
            justify="center",
            font=("Segoe UI",18),
            text_color="#374151"
        )

        self.live_text.pack(pady=20)
        # ===========================
        # Dashboard
        # ===========================

        self.dashboard = ctk.CTkFrame(
            self.left,
            fg_color="#EAF4FF",
            corner_radius=15
        )

        self.dashboard.pack(
            pady=20,
            padx=20,
            fill="x"
        )

        self.visitor_label = ctk.CTkLabel(
            self.dashboard,
            text="👥 Visitors Today : 0",
            font=("Segoe UI", 16, "bold")
        )

        self.visitor_label.pack(
            anchor="w",
            padx=15,
            pady=(15,5)
        )

        self.staff_label = ctk.CTkLabel(
            self.dashboard,
            text="👨‍💼 Staff Checked In : 0",
            font=("Segoe UI",16,"bold")
        )

        self.staff_label.pack(
            anchor="w",
            padx=15,
            pady=(0,15)
        )       
               # =====================================================
    # RIGHT PANEL
    # =====================================================

    def create_right_panel(self):

        self.right = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=20
        )

        self.right.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 20),
            pady=20
        )

        self.chat_frame = ctk.CTkScrollableFrame(
            self.right,
            fg_color="white"
        )

        self.chat_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )



    # =====================================================
    # CHAT BUBBLES
    # =====================================================

    def add_bubble(self, sender, message):

        is_user = sender == "You"

        bubble_color = "#1976D2" if is_user else "#ECEFF1"
        text_color = "white" if is_user else "#1F2937"

        outer = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )

        outer.pack(
            fill="x",
            pady=6,
            padx=5
        )

        bubble = ctk.CTkLabel(
            outer,
            text=message,
            wraplength=260,
            justify="left",
            padx=15,
            pady=12,
            corner_radius=18,
            fg_color=bubble_color,
            text_color=text_color,
            font=("Segoe UI", 14)
        )

        if is_user:
            bubble.pack(anchor="e")
        else:
            bubble.pack(anchor="w")

        # Auto-scroll to bottom
        self.after(
            100,
            lambda: self.chat_frame._parent_canvas.yview_moveto(1.0)
        )



    # =====================================================
    # BOT REPLY
    # =====================================================

     # =====================================================
    # BOT REPLY
    # =====================================================

    def bot_reply(self, message):

        self.live_text.configure(text=message)
        self.add_bubble("TinkRa", message)

        if self.is_speaking:
            return

        self.is_speaking = True
        self.set_status("🔊 Speaking...", "#0288D1")

        def run():
            speak(message)

            self.after(
                0,
                lambda: self.set_status("🟢 Ready", "#2E7D32")
            )

            self.is_speaking = False

        threading.Thread(target=run, daemon=True).start()


        # =====================================================
    # DASHBOARD
    # =====================================================

    def update_dashboard(self):

        self.visitor_label.configure(
            text=f"👥 Visitors Today : {get_visitor_count()}"
        )

        self.staff_label.configure(
            text=f"👨‍💼 Staff Checked In : {get_staff_count()}"
        )
    # =====================================================
    # STATUS
    # =====================================================

    def set_status(self, text, color):

        self.status_avatar.configure(
            text=text,
            text_color=color
        )

        self.status_top.configure(
            text=text
        )



    # =====================================================
    # CLOCK
    # =====================================================

    def update_time(self):

        now = datetime.now()

        self.time_label.configure(
            text=now.strftime("%d %b %Y   %I:%M:%S %p")
        )

        self.after(
            1000,
            self.update_time
        )



    # =====================================================
    # BOTTOM BAR
    # =====================================================

    def create_bottom(self):

        self.bottom = ctk.CTkFrame(
            self,
            fg_color="#F5F7FA",
            height=70
        )

        self.bottom.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0,20)
        )

        self.entry = ctk.CTkEntry(
            self.bottom,
            height=45,
            placeholder_text="Type your message..."
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(10,10),
            pady=10
        )

        self.entry.bind(
            "<Return>",
            lambda e: self.send_message()
        )

        self.mic_btn = ctk.CTkButton(
            self.bottom,
            text="🎤 Speak",
            width=120,
            command=self.voice_input
        )

        self.mic_btn.pack(
            side="left",
            padx=5
        )

        self.send_btn = ctk.CTkButton(
            self.bottom,
            text="📤 Send",
            width=120,
            command=self.send_message
        )

        self.send_btn.pack(
            side="left",
            padx=(5,10)
        )



    # =====================================================
    # SEND MESSAGE
    # =====================================================

    def send_message(self):

        text = self.entry.get().strip()

        if not text:
            return

        self.entry.delete(0, "end")

        self.add_bubble("You", text)

        self.set_status("🤔 Thinking...", "#F57C00")

        self.live_text.configure(text="Thinking...")

        response = get_response(text)
        self.update_dashboard()
        self.bot_reply(response)
            # =====================================================
    # VOICE INPUT
    # =====================================================

    def voice_input(self):

        self.set_status("🎤 Listening...", "#F57C00")

        self.live_text.configure(text="Listening...")

        def run():

            text = listen()

            print("Recognized:", repr(text))

            if text:

                self.after(
                    0,
                    lambda: self.entry.delete(0, "end")
                )

                self.after(
                    0,
                    lambda: self.entry.insert(0, text)
                )

                self.after(
                    300,
                    self.send_message
                )

            else:

                self.after(
                    0,
                    lambda: self.set_status("🟢 Ready", "#2E7D32")
                )

                self.after(
                    0,
                    lambda: self.live_text.configure(
                        text="I couldn't hear you. Please try again."
                    )
                )

        threading.Thread(
            target=run,
            daemon=True
        ).start()