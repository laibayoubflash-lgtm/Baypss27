import customtkinter as ctk
import requests
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BypassClientApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Baypss27 - Client Panel")
        self.geometry("450x380")
        self.resizable(False, False)

        self.title_label = ctk.CTkLabel(self, text="لوحة تحكم العميل", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=20)

        self.entry_serial = ctk.CTkEntry(self, placeholder_text="أدخل الرقم التسلسلي هنا...", width=350, height=40)
        self.entry_serial.pack(pady=10)

        self.btn_send = ctk.CTkButton(self, text="إرسال والتحقق", command=self.send_data_thread, width=200, height=40)
        self.btn_send.pack(pady=15)

        self.result_box = ctk.CTkTextbox(self, width=380, height=130, font=("Courier", 12))
        self.result_box.pack(pady=10)

    def send_data_thread(self):
        threading.Thread(target=self.send_request_to_server, daemon=True).start()

    def send_request_to_server(self):
        serial_val = self.entry_serial.get().strip()
        
        if not serial_val:
            self.result_box.delete("0.0", "end")
            self.result_box.insert("end", "خطأ: يرجى إدخال الرقم التسلسلي أولاً!\n")
            return

        self.result_box.delete("0.0", "end")
        self.result_box.insert("end", "جاري الاتصال بالسيرفر...\n")

        try:
            url = "https://baypss27.onrender.com/api/verify"
            payload = {"serial_number": serial_val}
            
            response = requests.post(url, json=payload, timeout=15)
            
            if response.status_code == 200:
                res_data = response.json()
                self.result_box.insert("end", "تم الاتصال بنجاح! ✅\n")
                self.result_box.insert("end", f"الرد: {res_data.get('message')}\n")
                self.result_box.insert("end", f"الحالة: {res_data.get('action')}\n")
            else:
                self.result_box.insert("end", f"خطأ من السيرفر: {response.status_code}\n")
                
        except requests.exceptions.RequestException:
            self.result_box.insert("end", "فشل الاتصال بالإنترنت أو بالسيرفر!\n")

if __name__ == "__main__":
    app = BypassClientApp()
    app.mainloop()
