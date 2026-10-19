import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
from PIL import Image, ImageTk
import os
from datetime import datetime

# ------------ الألوان الجديدة (Green Neon Theme) ------------
APP_BG = "#101820"             # خلفية رئيسية (أسود مائل للزرقة)
PANEL_BG = "#1A2B2F"           # خلفية الكروت (أزرق بترولي داكن)
ACCENT_COLOR = "#9EFF5C"       # اللون البارز (أخضر نيون)
SECONDARY_ACCENT = "#1ED4A3"   # تدرج ثانوي (سماوي مخضر)
TEXT_PRIMARY = "#EAEAEA"       # نصوص رئيسية (أبيض فاتح)
TEXT_SECONDARY = "#A8B2D1"     # نصوص ثانوية (رمادي مائل للزرقة)

TITLE_FONT = ("Arial", 30, "bold")
HEADER_FONT = ("Arial", 24, "bold")
BUTTON_FONT = ("Arial", 19, "bold")
BASE_FONT = ("Arial", 17, "bold")
SMALL_FONT = ("Arial", 15)

class EgyptianLaborLawExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("النظام الخبير لقانون العمل المصري")
        self.root.geometry("1200x800")
        self.root.configure(bg=APP_BG)

        self.topic_icons = {
            'annual_leave': '📅',
            'work_hours': '⏰',
            'end_of_service': '💰',
            'termination': '📄'
        }

        if not os.path.exists('data'):
            os.makedirs('data')

        self.knowledge_base = self.load_knowledge_base()
        self.user_data = {}
        self.log_entries = [] # لتخزين سجل الاستشارات
        self.topic_var = tk.StringVar(value="")

        self.setup_ui()

    def load_knowledge_base(self):
        knowledge_base = {
            "annual_leave": {
                "title": "الإجازة السنوية",
                "rules": [
                    "مادة (47): يستحق العامل إجازة سنوية مدتها 21 يوم بأجر عن كل سنة من سنوات الخدمة",
                    "مادة (48): تزاد الإجازة إلى 30 يومًا لمن أمضى في خدمة صاحب العمل عشر سنوات أو بلغ سن الخمسين",
                    "مادة (49): تجزأ الإجازة السنوية على النحو الذي تحدده لائحة العمل"
                ],
                "conditions": {"service_years": "عدد سنوات الخدمة", "age": "عمر العامل"}
            },
            "work_hours": {
                "title": "ساعات العمل والإضافي",
                "rules": [
                    "مادة (80): لا يجوز تشغيل العامل تشغيلاً فعلياً أكثر من 8 ساعات في اليوم أو 48 ساعة في الأسبوع",
                    "مادة (81): يكون أجر الساعة الواحدة عن العمل الإضافي مساوياً للأجر الأصلي مضافاً إليه 35% على الأقل",
                    "مادة (82): يمنح العامل راحة لا تقل عن ساعة بعد كل 5 ساعات عمل متواصلة"
                ],
                "conditions": {"daily_hours": "ساعات العمل اليومية", "overtime_hours": "ساعات العمل الإضافي"}
            },
            "end_of_service": {
                "title": "نهاية الخدمة والمكافأة",
                "rules": [
                    "مادة (112): يستحق العامل مكافأة عن مدة الخدمة تحسب على أساس أجر نصف شهر عن كل من السنوات الخمس الأولى",
                    "مادة (113): يستحق العامل مكافأة شهر كامل عن كل سنة من السنوات التالية",
                    "مادة (114): يحصل العامل على مكافأة نهاية الخدمة في حالة إنهاء العقد"
                ],
                "conditions": {"service_years": "عدد سنوات الخدمة", "last_salary": "آخر أجر شهري"}
            },
            "termination": {
                "title": "إنهاء عقد العمل",
                "rules": [
                    "مادة (110): لا يجوز لصاحب العمل فصل العامل دون مكافأة أو تعويض إلا في الحالات المنصوص عليها قانوناً",
                    "مادة (111): يحق للعامل الحصول على تعويض في حالة الفصل التعسفي",
                    "مادة (115): يجب إخطار العامل قبل الفصل بفترة معقولة أو تعويضه عن هذه الفترة"
                ],
                "conditions": {"termination_reason": "سبب إنهاء العقد", "service_years": "عدد سنوات الخدمة"}
            }
        }
        return knowledge_base

    def setup_ui(self):
        # ---------- الهيدر ----------
        header = tk.Frame(self.root, bg=PANEL_BG, height=90)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # --- شعار الميزان ---
        tk.Label(header, text="⚖️", font=("Arial", 48), bg=PANEL_BG, fg=ACCENT_COLOR).pack(side=tk.LEFT, padx=(30, 20), pady=10)

        tk.Label(header, text="النظام الخبير لقانون العمل المصري", font=TITLE_FONT, bg=PANEL_BG, fg=TEXT_PRIMARY).pack(side=tk.LEFT, pady=20)

        # --- زر عرض السجل في الهيدر ---
        header_right_frame = tk.Frame(header, bg=PANEL_BG)
        header_right_frame.pack(side=tk.RIGHT, padx=30)

        tk.Button(header_right_frame, text="📜 عرض السجل", font=("Arial", 14, "bold"), bg=SECONDARY_ACCENT, fg=APP_BG,
                  relief=tk.RAISED, bd=2, padx=15, pady=5, command=self.show_log_window).pack(side=tk.RIGHT, padx=10)

        tk.Label(header_right_frame, text="نسخة تجريبية", font=SMALL_FONT, bg=PANEL_BG, fg=TEXT_SECONDARY).pack(side=tk.RIGHT, padx=10)

        # ---------- الإطار الرئيسي ----------
        main = tk.Frame(self.root, bg=APP_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # ---------- السايدبار ----------
        sidebar = tk.Frame(main, bg=PANEL_BG, width=340, relief=tk.SOLID, bd=1, highlightbackground=ACCENT_COLOR, highlightthickness=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="المواضيع القانونية", font=HEADER_FONT, bg=PANEL_BG, fg=TEXT_PRIMARY).pack(pady=(40, 30))

        topics = [
            ("الإجازة السنوية", "annual_leave"),
            ("ساعات العمل", "work_hours"),
            ("نهاية الخدمة والمكافأة", "end_of_service"),
            ("إنهاء عقد العمل", "termination")
        ]

        for name, key in topics:
            card = tk.Frame(sidebar, bg=PANEL_BG, relief=tk.SOLID, bd=1, highlightbackground="#333")
            card.pack(fill=tk.X, padx=30, pady=12)
            inner = tk.Frame(card, bg=PANEL_BG)
            inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)
            tk.Label(inner, text=self.topic_icons[key], font=("Arial", 26), bg=PANEL_BG, fg=ACCENT_COLOR).pack(side=tk.LEFT, padx=(0, 20))
            tk.Button(inner, text=name, font=BASE_FONT, bg=PANEL_BG, fg=TEXT_PRIMARY,
                      relief=tk.FLAT, anchor="w", command=lambda k=key: self.set_topic(k)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # ---------- المنطقة الرئيسية ----------
        right = tk.Frame(main, bg=APP_BG)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # الكارت الرئيسي (الحالة الافتراضية)
        self.main_card = tk.Frame(right, bg=PANEL_BG, relief=tk.RAISED, bd=2)
        self.main_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=0)

        tk.Label(self.main_card, text="🗂️", font=("Arial", 120), bg=PANEL_BG, fg=ACCENT_COLOR).pack(pady=(80, 40))

        tk.Label(self.main_card, text="مرحبا بك في النظام الخبير لقانون العمل المصري",
                 font=("Arial", 22, "bold"), bg=PANEL_BG, fg=TEXT_PRIMARY).pack()

        tk.Label(self.main_card, text="اختر موضوعاً من القائمة اليسرى للحصول على استشارة قانونية سريعة\nبناءً على أحكام قانون العمل المصري",
                 font=BASE_FONT, bg=PANEL_BG, fg=TEXT_SECONDARY, justify=tk.CENTER).pack(pady=30)

        # منطقة المحتوى الديناميكي (سيتم استبدال الكارت الرئيسي بها عند اختيار موضوع)
        self.dynamic_area = tk.Frame(right, bg=APP_BG)

        # --- إطار الأزرار (تم نقله هنا ليكون دائماً ظاهراً) ---
        buttons_frame = tk.Frame(right, bg=APP_BG)
        buttons_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 20), padx=20)

        # الأزرار الثلاثة الكبيرة
        self.save_btn = tk.Button(buttons_frame, text="حفظ الاستشارة", font=BUTTON_FONT, bg=SECONDARY_ACCENT, fg=TEXT_PRIMARY,
                                  relief=tk.RAISED, bd=3, padx=30, pady=14, command=self.save_consultation)
        self.save_btn.pack(side=tk.LEFT, expand=True, padx=10)

        self.clear_btn = tk.Button(buttons_frame, text="مسح النموذج", font=BUTTON_FONT, bg="#4A4A4A", fg=TEXT_PRIMARY,
                                   relief=tk.RAISED, bd=3, padx=30, pady=14, command=self.clear_form)
        self.clear_btn.pack(side=tk.LEFT, expand=True, padx=10)

        self.consult_btn = tk.Button(buttons_frame, text="استشارة قانونية", font=BUTTON_FONT, bg=ACCENT_COLOR, fg="#101820",
                                     relief=tk.RAISED, bd=3, padx=30, pady=14, state=tk.DISABLED, command=self.provide_consultation)
        self.consult_btn.pack(side=tk.LEFT, expand=True, padx=10)

    def set_topic(self, key):
        self.topic_var.set(key)
        self.show_topic_content()

    def show_topic_content(self):
        topic_key = self.topic_var.get()
        topic = self.knowledge_base.get(topic_key)
        if not topic: return

        # إخفاء الكارت الافتراضي
        self.main_card.pack_forget()

        # إظهار منطقة المحتوى الديناميكي
        self.dynamic_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=0)

        for widget in self.dynamic_area.winfo_children():
            widget.destroy()

        # كارت المواد والحقول
        content_card = tk.Frame(self.dynamic_area, bg=PANEL_BG)
        content_card.pack(fill=tk.BOTH, expand=True)

        # عنوان الموضوع
        tk.Label(content_card, text=f"{self.topic_icons[topic_key]}  {topic['title']}", font=("Arial", 20, "bold"),
                 bg=PANEL_BG, fg=TEXT_PRIMARY).pack(pady=(30,20))

        # المواد القانونية
        rules_text = scrolledtext.ScrolledText(content_card, height=8, font=BASE_FONT, wrap=tk.WORD, bg=APP_BG, fg=TEXT_SECONDARY, relief=tk.FLAT, bd=0)
        rules_text.pack(fill=tk.X, padx=50, pady=(0,20))
        for rule in topic['rules']:
            rules_text.insert(tk.END, f"• {rule}\n\n")
        rules_text.config(state=tk.DISABLED)

        # حقول الإدخال
        input_frame = tk.Frame(content_card, bg=PANEL_BG)
        input_frame.pack(fill=tk.X, padx=100, pady=20)

        self.input_vars = {}
        for key, label in topic['conditions'].items():
            row = tk.Frame(input_frame, bg=PANEL_BG)
            row.pack(fill=tk.X, pady=12)
            tk.Label(row, text=f"{label} :", font=BASE_FONT, bg=PANEL_BG, fg=TEXT_PRIMARY, width=25, anchor="e").pack(side=tk.RIGHT)
            var = tk.StringVar()
            entry = tk.Entry(row, textvariable=var, font=BASE_FONT, relief=tk.SOLID, bd=1, bg=APP_BG, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=20)
            self.input_vars[key] = var

        self.consult_btn.config(state=tk.NORMAL)

    def provide_consultation(self):
        topic_key = self.topic_var.get()
        topic = self.knowledge_base[topic_key]

        user_data = {}
        for key, var in self.input_vars.items():
            val = var.get().strip()
            if not val:
                messagebox.showwarning("ناقص", f"يرجى إدخال {topic['conditions'][key]}")
                return
            user_data[key] = val

        consultation = self.generate_consultation(topic_key, user_data)

        # عرض النتيجة
        for widget in self.dynamic_area.winfo_children():
            widget.destroy()

        result_card = tk.Frame(self.dynamic_area, bg=PANEL_BG)
        result_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(result_card, text=f"✅ نتيجة الاستشارة: {topic['title']}", font=("Arial", 20, "bold"),
                 bg=PANEL_BG, fg=ACCENT_COLOR).pack(pady=(30,20))

        result_text = scrolledtext.ScrolledText(result_card, font=BASE_FONT, wrap=tk.WORD, bg=APP_BG, fg=TEXT_SECONDARY, relief=tk.FLAT, bd=0)
        result_text.pack(fill=tk.BOTH, expand=True, padx=50, pady=(0,30))

        output = "البيانات المدخلة:\n"
        for k, v in user_data.items():
            output += f"   • {topic['conditions'][k]}: {v}\n"
        output += "\nالاستشارة القانونية:\n\n"
        output += consultation
        output += "\n\n⚠️ ملاحظة: هذه استشارة آلية أولية، يُرجى استشارة محامٍ متخصص."

        result_text.insert(tk.END, output)
        result_text.config(state=tk.DISABLED)

        self.user_data = user_data
        self.add_to_log(topic['title'], consultation)

    def generate_consultation(self, topic_key, data):
        try:
            if topic_key == "annual_leave":
                years = int(data['service_years'])
                age = int(data['age'])
                if years >= 10 or age >= 50:
                    return "تستحق إجازة سنوية مدتها 30 يومًا بأجر كامل."
                elif years >= 1:
                    return "تستحق إجازة سنوية مدتها 21 يومًا بأجر كامل."
                else:
                    return "تستحق إجازة بنسبة عن المدة المقضية (حوالي 1.75 يوم لكل شهر)."

            elif topic_key == "work_hours":
                daily = float(data['daily_hours'])
                ot = float(data['overtime_hours'])
                msg = ""
                if daily > 8:
                    msg += f"تحذير: تجاوز الحد القانوني بـ {daily-8} ساعة يوميًا.\n"
                if ot > 0:
                    msg += f"تستحق أجر إضافي بنسبة لا تقل عن 35% عن {ot} ساعة.\n"
                return msg or "ساعات العمل ضمن الحدود القانونية."

            elif topic_key == "end_of_service":
                years = int(data['service_years'])
                salary = float(data['last_salary'])
                if years <= 5:
                    reward = salary * 0.5 * years
                else:
                    reward = salary * 0.5 * 5 + salary * (years - 5)
                return f"المكافأة المستحقة: {reward:,.2f} جنيه مصري."

            elif topic_key == "termination":
                reason = data['termination_reason']
                if any(word in reason for word in ['تعسفي', 'بدون سبب', 'فصل تعسفي']):
                    return "يُعتبر الفصل تعسفيًا ويحق لك تعويض لا يقل عن أجر شهرين عن كل سنة خدمة."
                else:
                    return "حسب السبب، قد لا تستحق تعويضًا كاملاً. يُفضل مراجعة محامٍ."
        except:
            return "خطأ في البيانات المدخلة. تأكد من استخدام أرقام صحيحة."

        return "لا توجد استشارة."

    def show_log_window(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("📜 سجل الاستشارات")
        log_window.geometry("700x500")
        log_window.configure(bg=APP_BG)
        log_window.transient(self.root) # لتبقى فوق النافذة الرئيسية
        log_window.grab_set() # لجعل التفاعل محصوراً بها حتى تغلق

        tk.Label(log_window, text="سجل الاستشارات المحفوظة", font=HEADER_FONT, bg=APP_BG, fg=TEXT_PRIMARY).pack(pady=20)

        log_text_widget = scrolledtext.ScrolledText(log_window, font=BASE_FONT, wrap=tk.WORD, bg=PANEL_BG, fg=TEXT_SECONDARY, relief=tk.SOLID, bd=1)
        log_text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        if not self.log_entries:
            log_text_widget.insert(tk.END, "لا توجد استشارات مسجلة بعد.", "center")
        else:
            for entry in self.log_entries:
                log_text_widget.insert(tk.END, entry)

        log_text_widget.config(state=tk.DISABLED)

        close_button = tk.Button(log_window, text="إغلاق", font=BUTTON_FONT, bg=SECONDARY_ACCENT, fg=APP_BG, relief=tk.RAISED, bd=2, command=log_window.destroy)
        close_button.pack(pady=15, padx=20)

    def add_to_log(self, topic, consultation):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"--- [ {timestamp} ] ---\n"
        entry += f"الموضوع: {topic}\n\n"
        entry += "الاستشارة:\n" + consultation + "\n"
        entry += "--------------------------------------------------\n\n"
        self.log_entries.append(entry)

    def clear_form(self):
        self.topic_var.set("")
        self.consult_btn.config(state=tk.DISABLED)
        self.dynamic_area.pack_forget()
        self.main_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=0)

    def save_consultation(self):
        if not self.user_data:
            messagebox.showinfo("حفظ", "لا توجد استشارة لحفظها.")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/consultation_{timestamp}.json"
        data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "topic": self.knowledge_base[self.topic_var.get()]["title"],
            "user_data": self.user_data,
            "consultation": "تم الحفظ (النتيجة موجودة في الواجهة)"
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("نجاح", f"تم الحفظ في:\n{filename}")

def main():
    root = tk.Tk()
    app = EgyptianLaborLawExpertSystem(root)
    root.update_idletasks()
    w, h = 1200, 800
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.mainloop()

if __name__ == "__main__":
    main()