import tkinter as tk
from tkinter import ttk, messagebox
from database import db
from utils import clear

def add_category_page(main):
    # ၁။ စာမျက်နှာဟောင်းများကို ဖယ်ရှားခြင်း
    clear(main)
    main.config(bg="#f8f9fa")

    # ဒေတာဘေ့စ်ထဲမှာ categories table မရှိသေးရင် ဆောက်ရန်
    conn = db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cat_name TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

    # ခေါင်းစဉ်ကြီး
    tk.Label(
        main, 
        text="📁 Category Management", 
        font=("Segoe UI", 22, "bold"), 
        fg="#2c3e50", 
        bg="#f8f9fa"
    ).pack(pady=15)

    # 🌟 [ပင်မ Container Frame] - ဘယ်/ညာ Panel နှစ်ခုကို ကပ်ထားမည့် နေရာ
    main_container = tk.Frame(main, bg="#f8f9fa")
    main_container.pack(fill="both", expand=True, padx=20, pady=10)

    # =================================================================
    # 👈 ဘယ်ဘက် Panel: ADD CATEGORY FORM
    # =================================================================
    left_panel = tk.LabelFrame(
        main_container, 
        text="Add New Category", 
        font=("Segoe UI", 12, "bold"),
        fg="#2c3e50", 
        bg="white", 
        relief="solid", 
        bd=1
    )
    left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)

    tk.Label(
        left_panel, 
        text="Category Name:", 
        font=("Segoe UI", 11, "bold"), 
        fg="#34495e", 
        bg="white"
    ).pack(anchor="w", padx=20, pady=(30, 5))

    cat_entry = tk.Entry(left_panel, font=("Segoe UI", 12), relief="solid", bd=1)
    cat_entry.pack(fill="x", padx=20, pady=5, ipady=4)

    # =================================================================
    # =================================================================
    # 👉 ညာဘက် Panel: CATEGORY LIST (Medicine List စတိုင်လ် ပြောင်းလဲထားခြင်း)
    # =================================================================
    right_panel = tk.LabelFrame(
        main_container, 
        text="Existing Categories", 
        font=("Segoe UI", 12, "bold"),
        fg="#2c3e50", 
        bg="white", 
        relief="solid", 
        bd=1
    )
    right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=5)

    # 🌟 [ဒီဇိုင်း Style သတ်မှတ်ခြင်း] Medicine List အတိုင်း ကွက်တိဖြစ်စေရန်
    cat_style = ttk.Style()
    cat_style.theme_use("clam")
    cat_style.configure("Cat.Treeview", font=("Segoe UI", 10, "bold"), rowheight=28, background="white")
    cat_style.configure("Cat.Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#34495e", foreground="white")
    cat_style.map("Cat.Treeview", background=[("selected", "#1abc9c")]) # ရွေးလိုက်ရင် စိမ်းပြာရောင်ပြောင်းမည်

    # Table Container Frame
    tree_frame = tk.Frame(right_panel)
    tree_frame.pack(fill="both", expand=True, padx=15, pady=15)

    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side="right", fill="y")

    # 🌟 style="Cat.Treeview" ကို ချိတ်ဆက်ပေးလိုက်ပါတယ်
    tree = ttk.Treeview(
        tree_frame, 
        columns=("id", "name"), 
        show="headings", 
        style="Cat.Treeview", 
        yscrollcommand=scrollbar.set
    )
    scrollbar.config(command=tree.yview)

    # Column ခေါင်းစဉ်များနှင့် အလယ်တည့်တည့် နေရာချခြင်း
    tree.heading("id", text="No.", anchor="center")
    tree.heading("name", text="Category Name", anchor="center")
    
    # 🌟 အကွက်အကျယ်နှင့် စာသား alignment ကို စနစ်တကျ ညှိခြင်း
    tree.column("id", width=80, anchor="center")
    tree.column("name", width=260, anchor="w") # Category နာမည်ကို ဘယ်ဘက်ကပ်ထားပြီး ပတ်ဝန်းကျင် Space ချန်ထားပါတယ်
    
    tree.pack(fill="both", expand=True)

    # 🔄 Database ထဲက Category များကို ဆွဲထုတ်ပြသမည့် Function
    def load_categories():
        for item in tree.get_children():
            tree.delete(item)
        
        conn = db()
        c = conn.cursor()
        c.execute("SELECT id, cat_name FROM categories ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()

        for idx, row in enumerate(rows, 1):
            tree.insert("", "end", values=(idx, row[1]))

    # 💾 Category အသစ်ထည့်မည့် အလုပ်လုပ်ချက်
    def save_category():
        cat_name = cat_entry.get().strip()
        if not cat_name:
            messagebox.showwarning("Warning", "Please enter a category name!")
            return

        try:
            conn = db()
            c = conn.cursor()
            c.execute("INSERT INTO categories (cat_name) VALUES (?)", (cat_name,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"'{cat_name}' added successfully!")

            cat_entry.delete(0, tk.END) # ရိုက်ထားတဲ့ စာသားကို ပြန်ဖျက်မယ်
            load_categories() # ညာဘက် ဇယားကို ချက်ချင်း Update လုပ်မယ်
            
        except tk.sqlite3.IntegrityError:
            messagebox.showerror("Error", "This category already exists!")

    # Save Button (ဘယ်ဘက် Form အောက်တွင် ပြသရန်)
    tk.Button(
        left_panel, 
        text="➕ Add Category", 
        font=("Segoe UI", 11, "bold"), 
        bg="#2ecc71", 
        fg="white", 
        relief="flat",
        command=save_category
    ).pack(fill="x", padx=20, pady=20, ipady=4)

    # စာမျက်နှာပွင့်လာတာနဲ့ ညာဘက်ဇယားထဲ ဒေတာအလိုအလျောက်ဖြည့်ရန်
    load_categories()