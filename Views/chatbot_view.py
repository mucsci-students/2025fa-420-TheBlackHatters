import customtkinter as ctk
import threading
from typing import Any
from Controller.chatbot_agent import ChatbotAgent
from Controller.main_controller import configImportBTN, configExportBTN


class ChatbotView(ctk.CTkFrame):
    def __init__(self, master: Any):
        super().__init__(master)

        # Acquire config path from main app
        app: Any = self.winfo_toplevel()
        if hasattr(app, "configPath"):
            self.configPath = app.configPath
        else:
            # fallback if opened independently
            from tkinter import StringVar

            self.configPath = StringVar()
            self.configPath.set(
                "Start editing this new Config File or Import your own. Press export to save new changes."
            )

        # --- normalize to tkinter.Variable ---
        from tkinter import StringVar, Variable

        if not isinstance(self.configPath, Variable):
            val = str(getattr(self.configPath, "get", lambda: self.configPath)())
            self.configPath = StringVar(value=val)

        # Function to retrieve current config path
        def get_config_path() -> str:
            from tkinter import Variable

            if isinstance(self.configPath, Variable):
                return self.configPath.get()  # type: ignore[union-attr]
            return str(self.configPath)

        # Initialize chatbot agent
        self.agent = ChatbotAgent(get_config_path)

        # Header Frame (replicates Edit Config layout)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=5)

        # Import button
        import_btn = ctk.CTkButton(
            header_frame,
            text="Import Config",
            width=150,
            command=lambda: configImportBTN(
                self.configPath, getattr(app, "refresh", None)
            ),
        )
        import_btn.pack(side="left", padx=(0, 10))

        # Path entry
        path_entry = ctk.CTkEntry(
            header_frame,
            state="readonly",
            textvariable=self.configPath,  # guaranteed StringVar
            width=500,
        )
        path_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # Export button
        export_btn = ctk.CTkButton(
            header_frame,
            text="Export Config",
            width=150,
            command=lambda: configExportBTN(self.configPath),
        )
        export_btn.pack(side="left", padx=(0, 10))

        # Chat display
        self.chat_display = ctk.CTkTextbox(self, width=700, height=400)
        try:
            self.chat_display.configure(font=("Menlo", 12))
        except Exception:
            self.chat_display.configure(font=("Courier", 12))
        self.chat_display.pack(pady=10, padx=10, fill="both", expand=True)
        self.chat_display.configure(state="disabled")

        # Input row
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.entry = ctk.CTkEntry(
            input_frame, placeholder_text="Ask the scheduler assistant…"
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self._on_enter_pressed)

        self.send_button = ctk.CTkButton(
            input_frame, text="Send", width=80, command=self.send_message
        )
        self.send_button.pack(side="right")

        # Initial greeting
        self._append_text(
            "Bot: Hi! I’m your schedule assistant.\n"
            "I can:\n"
            "• Show the current configuration (summary)\n"
            "• Make changes (e.g., “remove Mac lab from CMSC 330”)\n"
            "• Explain what fields mean\n\n"
            "Try: “View current config” or “Change CMSC 330 to not use Mac lab”.\n\n"
        )

    def _on_enter_pressed(self, event):
        self.send_message()
        return "break"

    def _append_text(self, text: str):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text)
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def send_message(self):
        user_message = self.entry.get().strip()
        if not user_message:
            return

        self._append_text(f"You: {user_message}\n")

        def worker():
            response = self.agent.query(user_message)
            self.after(0, lambda: self._append_text(f"Bot:\n{response}\n\n\n"))

        threading.Thread(target=worker, daemon=True).start()
        self.entry.delete(0, "end")
