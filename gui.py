import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
import requests

API_BASE = "http://127.0.0.1:5000"

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        root.title("📚 Pustaklok")
        root.geometry("1000x750")
        root.minsize(800, 600)
        
        # Configure colors - Modern dark theme
        self.bg_color = "#0f0f1e"
        self.accent_color = "#6366f1"
        self.accent_light = "#818cf8"
        self.text_color = "#f1f5f9"
        self.list_bg = "#1e293b"
        self.button_bg = "#4f46e5"
        self.hover_color = "#a78bfa"
        self.success_color = "#10b981"
        self.error_color = "#ef4444"
        
        root.configure(bg=self.bg_color)
        self.configure_styles()
        self.create_widgets()
        self.setup_bindings()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for ttk widgets
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=('Segoe UI', 10))
        style.configure('Header.TLabel', background=self.bg_color, foreground=self.accent_light, font=('Segoe UI', 16, 'bold'))
        style.configure('Section.TLabel', background=self.bg_color, foreground=self.accent_light, font=('Segoe UI', 11, 'bold'))
        style.configure('TButton', font=('Segoe UI', 9, 'bold'), padding=8)
        style.configure('Accent.TButton', font=('Segoe UI', 9, 'bold'), padding=10)
        style.configure('TCombobox', fieldbackground=self.list_bg, background=self.bg_color, foreground=self.text_color, font=('Segoe UI', 10))
        style.configure('TEntry', fieldbackground=self.list_bg, foreground=self.text_color, font=('Segoe UI', 10), padding=5)
        
        style.map('Accent.TButton',
                 background=[('active', self.hover_color)],
                 foreground=[('active', self.bg_color)])
        
        # Scrollbar styling
        style.configure('Vertical.TScrollbar', background=self.bg_color, troughcolor=self.list_bg)

    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header with gradient effect using frame
        header_frame = tk.Frame(main_frame, bg=self.accent_color, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 0))
        header_frame.pack_propagate(False)
        
        header = tk.Label(header_frame, text="📚 Pustaklok - Digital Library", 
                         bg=self.accent_color, fg="white", font=('Segoe UI', 18, 'bold'), pady=15)
        header.pack()
        
        subtitle = tk.Label(header_frame, text="Organize and manage your media collection", 
                           bg=self.accent_color, fg="#e0e7ff", font=('Segoe UI', 10))
        subtitle.pack()
        
        # Content frame with padding
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Quick Actions Frame with better styling
        action_frame = ttk.LabelFrame(content_frame, text="🚀 Quick Actions", padding=15)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_container = ttk.Frame(action_frame)
        btn_container.pack(fill=tk.X)
        
        ttk.Button(btn_container, text="🔄 Load All", command=self.load_all, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_container, text="➕ Add Item", command=self.create_new, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_container, text="🗑️  Remove", command=self.delete_selected, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_container, text="🔄 Refresh", command=self.load_all, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_container, text="📤 Borrow", command=self.borrow_item, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_container, text="📥 Return", command=self.return_item, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        # Search and Filter Frame
        search_frame = ttk.LabelFrame(content_frame, text="🔍 Search & Filter", padding=15)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Category section with label
        cat_label = ttk.Label(search_frame, text="Filter by Category:", style='Section.TLabel')
        cat_label.pack(side=tk.LEFT, padx=(0, 12))
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(search_frame, textvariable=self.category_var, 
                                          values=["Book","Film","Magazine"], width=15, state="readonly")
        self.category_combo.pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(search_frame, text="🔎 Filter", command=self.load_category).pack(side=tk.LEFT, padx=(0, 20))
        
        # Search by title
        search_label = ttk.Label(search_frame, text="Search Title:", style='Section.TLabel')
        search_label.pack(side=tk.LEFT, padx=(0, 12))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 8))
        search_entry.bind('<Return>', lambda e: self.search_name())
        
        ttk.Button(search_frame, text="🔍 Search", command=self.search_name).pack(side=tk.LEFT)
        
        # Results Frame with info
        results_info = ttk.Frame(content_frame)
        results_info.pack(fill=tk.X, pady=(0, 8))
        
        results_label = ttk.Label(results_info, text="📖 Library Items (Double-click for details)", style='Section.TLabel')
        results_label.pack(side=tk.LEFT)
        
        self.count_label = ttk.Label(results_info, text="", foreground=self.accent_color)
        self.count_label.pack(side=tk.RIGHT)
        
        # Results Frame with scrollbar
        results_frame = ttk.Frame(content_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(results_frame, 
                                  width=120, 
                                  height=18,
                                  bg=self.list_bg,
                                  fg=self.text_color,
                                  font=('Consolas', 10),
                                  yscrollcommand=scrollbar.set,
                                  activestyle='none',
                                  selectmode=tk.SINGLE,
                                  highlightthickness=0,
                                  relief=tk.FLAT,
                                  borderwidth=0)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind("<Double-Button-1>", self.show_metadata)
        self.listbox.bind("<Delete>", lambda e: self.delete_selected())
        
        # Status bar with info
        status_frame = ttk.Frame(content_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="🟢 Ready", foreground=self.success_color, font=('Segoe UI', 10, 'bold'))
        self.status_label.pack(side=tk.LEFT)
        
        self.info_label = ttk.Label(status_frame, text="", foreground=self.accent_color, font=('Segoe UI', 9))
        self.info_label.pack(side=tk.RIGHT)
    
    def setup_bindings(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-l>', lambda e: self.load_all())
        self.root.bind('<Control-n>', lambda e: self.create_new())
        self.root.bind('<Control-f>', lambda e: self.search_var.focus())

    def load_all(self):
        try:
            self.status_label.config(text="🔄 Loading all items...")
            self.root.update()
            r = requests.get(f"{API_BASE}/media", timeout=3)
            r.raise_for_status()
            items = r.json()
            self.populate_list(items)
            count = len(items)
            self.status_label.config(text=f"🟢 Ready", foreground=self.success_color)
            self.count_label.config(text=f"Total: {count} items")
        except Exception as e:
            self.status_label.config(text="🔴 Error loading items", foreground=self.error_color)
            self.info_label.config(text=f"Connection failed: {str(e)[:50]}")
            messagebox.showerror("Connection Error", f"Could not connect to server:\n{e}")

    def load_category(self):
        cat = self.category_var.get().strip()
        if not cat:
            messagebox.showwarning("Warning","Please select a category first")
            return
        try:
            self.status_label.config(text=f"🔄 Loading {cat}...")
            self.root.update()
            r = requests.get(f"{API_BASE}/media/category/{cat}", timeout=3)
            r.raise_for_status()
            items = r.json()
            self.populate_list(items)
            count = len(items)
            self.status_label.config(text=f"🟢 Ready", foreground=self.success_color)
            self.count_label.config(text=f"Filtered: {count} items in {cat}")
        except Exception as e:
            self.status_label.config(text="🔴 Filter error", foreground=self.error_color)
            messagebox.showerror("Error", f"Could not load category: {e}")

    def search_name(self):
        name = self.search_var.get().strip()
        if not name:
            messagebox.showwarning("Warning","Enter a title to search")
            return
        try:
            self.status_label.config(text=f"🔄 Searching for '{name}'...")
            self.root.update()
            r = requests.get(f"{API_BASE}/media/search", params={"name":name}, timeout=3)
            if r.status_code == 404:
                self.status_label.config(text="🟡 Not found", foreground=self.accent_color)
                self.count_label.config(text="0 results")
                self.listbox.delete(0, tk.END)
                self.listbox.insert(tk.END, f"  No items found matching: '{name}'")
                return
            r.raise_for_status()
            item = r.json()
            self.populate_list([item])
            self.status_label.config(text="🟢 Ready", foreground=self.success_color)
            self.count_label.config(text="1 result found")
        except Exception as e:
            self.status_label.config(text="🔴 Search error", foreground=self.error_color)
            messagebox.showerror("Error", f"Search failed: {e}")

    def populate_list(self, items):
        self.listbox.delete(0, tk.END)
        if not items:
            self.listbox.insert(tk.END, "  ℹ️  No results found. Try another search or load all items.")
            return
        for idx, it in enumerate(items, 1):
            name = it.get('name', 'N/A')
            category = it.get('category', 'N/A')
            author = it.get('author', 'N/A')
            date = it.get('publication_date', 'N/A')
            available = it.get('available', True)
            borrowed_by = it.get('borrowed_by')
            
            # Color-coded by category
            emoji = self._get_category_emoji(category)
            status = "✓ Available" if available else f"✗ Borrowed by {borrowed_by}"
            display = f"{idx:3d}. {emoji} {name[:28]:<28} • {author[:18]:<18} • {date} [{status}]"
            self.listbox.insert(tk.END, display)
    
    def _get_category_emoji(self, category):
        """Return emoji based on category"""
        emojis = {"Book": "📕", "Film": "🎬", "Magazine": "📰"}
        return emojis.get(category, "📄")

    def create_new(self):
        """Open a dialog to create a new library item and POST to backend."""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Add New Item to Library")
        dialog.geometry("420x360")
        dialog.configure(bg=self.bg_color)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        content = ttk.Frame(dialog)
        content.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

        fields = {}
        field_configs = [
            ("Title", "title"),
            ("Author/Director", "author"),
            ("Publication Date (YYYY-MM-DD)", "date"),
            ("Category (Book/Film/Magazine)", "category"),
        ]

        for label_text, field_name in field_configs:
            label = ttk.Label(content, text=label_text + ":")
            label.pack(anchor=tk.W, pady=(12 if label_text == "Title" else 8, 4))
            entry = ttk.Entry(content, width=36)
            entry.pack(anchor=tk.W)
            fields[field_name] = entry

        btn_frame = ttk.Frame(content)
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        def save():
            name = fields["title"].get().strip()
            author = fields["author"].get().strip()
            pub = fields["date"].get().strip()
            cat = fields["category"].get().strip()

            if not all([name, author, pub, cat]):
                messagebox.showwarning("Missing Fields", "Please fill all fields")
                return

            payload = {"name": name, "author": author, "publication_date": pub, "category": cat}
            try:
                self.status_label.config(text="🔄 Creating item...")
                self.root.update()
                r = requests.post(f"{API_BASE}/media", json=payload, timeout=3)
                if r.status_code == 201:
                    messagebox.showinfo("✓ Success", f"Item '{name}' added to library!")
                    dialog.destroy()
                    self.load_all()
                else:
                    messagebox.showerror("Error", f"Could not create item:\n{r.text}")
                    self.status_label.config(text="🔴 Creation failed", foreground=self.error_color)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create item:\n{e}")
                self.status_label.config(text="🔴 Creation failed", foreground=self.error_color)

        ttk.Button(btn_frame, text="✅ Save", command=save, style='Accent.TButton').pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy).pack(side=tk.LEFT)

    def get_selected_name(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        text = self.listbox.get(sel[0])
        # Extract name from format: "idx. emoji name • author • date [status]"
        # Split by " • " to get parts
        parts = text.split(" • ")
        if len(parts) > 0:
            first_part = parts[0]  # Contains "idx. emoji name"
            # Remove leading numbers, dots, spaces, and emoji
            name_start = 0
            for i, char in enumerate(first_part):
                if char.isalpha():  # First alphabetic character marks start of name
                    name_start = i
                    break
            return first_part[name_start:].strip()
        return None

    def show_metadata(self, event=None):
        name = self.get_selected_name()
        if not name:
            return
        try:
            r = requests.get(f"{API_BASE}/media/{name}", timeout=3)
            if r.status_code == 404:
                messagebox.showinfo("Not found", "No metadata found for this item")
                return
            r.raise_for_status()
            item = r.json()
            
            # Format detailed info
            info_text = f"""
╔══════════════════════════════════════╗
║          ITEM DETAILS                ║
╚══════════════════════════════════════╝

Title:             {item.get('name', 'N/A')}
Author:            {item.get('author', 'N/A')}
Category:          {item.get('category', 'N/A')}
Publication Date:  {item.get('publication_date', 'N/A')}
            """
            
            messagebox.showinfo(f"📋 Details: {name}", info_text)
            self.status_label.config(text=f"🟢 Ready", foreground=self.success_color)
            self.info_label.config(text=f"Viewing: {name}")
        except Exception as e:
            self.status_label.config(text="🔴 Error fetching metadata", foreground=self.error_color)
            messagebox.showerror("Error", f"Could not fetch metadata: {e}")

    def delete_selected(self):
        name = self.get_selected_name()
        if not name:
            messagebox.showwarning("Warning","Select an item to delete")
            return
        
        if not messagebox.askyesno("⚠️ Confirm Delete", f"Are you sure you want to delete:\n\n'{name}'?\n\nThis cannot be undone."):
            return
        
        try:
            self.status_label.config(text="🔄 Deleting item...")
            self.root.update()
            r = requests.delete(f"{API_BASE}/media/{name}", timeout=3)
            if r.status_code == 200:
                self.status_label.config(text="🟢 Ready", foreground=self.success_color)
                messagebox.showinfo("✓ Deleted",f"Item '{name}' has been removed")
                self.load_all()
            else:
                self.status_label.config(text="🔴 Delete error", foreground=self.error_color)
                messagebox.showerror("Error", f"Could not delete: {r.text}")
        except Exception as e:
            self.status_label.config(text="🔴 Error deleting", foreground=self.error_color)
            messagebox.showerror("Error", f"Delete failed: {e}")

    def borrow_item(self):
        """Borrow a selected item."""
        name = self.get_selected_name()
        if not name:
            messagebox.showwarning("Warning", "Select an item to borrow")
            return
        
        name = name.strip()  # Ensure no trailing spaces
        
        borrower = simpledialog.askstring("👤 Borrow Item", f"Who is borrowing '{name}'?\n\nEnter name:")
        if not borrower:
            return
        
        borrower = borrower.strip()
        
        try:
            self.status_label.config(text="🔄 Borrowing item...")
            self.root.update()
            payload = {"borrower": borrower}
            # URL encode the name to handle special characters
            from urllib.parse import quote
            encoded_name = quote(name, safe='')
            r = requests.post(f"{API_BASE}/media/{encoded_name}/borrow", json=payload, timeout=3)
            if r.status_code == 200:
                self.status_label.config(text="🟢 Ready", foreground=self.success_color)
                messagebox.showinfo("✓ Borrowed", f"'{name}' borrowed by {borrower}")
                self.load_all()
            else:
                self.status_label.config(text="🔴 Borrow error", foreground=self.error_color)
                error_msg = r.json().get("error", r.text) if r.status_code != 500 else r.text
                messagebox.showerror("Error", f"Could not borrow: {error_msg}")
        except Exception as e:
            self.status_label.config(text="🔴 Error borrowing", foreground=self.error_color)
            messagebox.showerror("Error", f"Borrow failed: {str(e)}")

    def return_item(self):
        """Return a borrowed item."""
        name = self.get_selected_name()
        if not name:
            messagebox.showwarning("Warning", "Select an item to return")
            return
        
        name = name.strip()  # Ensure no trailing spaces
        
        if not messagebox.askyesno("📥 Return Item", f"Return '{name}' to the library?"):
            return
        
        try:
            self.status_label.config(text="🔄 Returning item...")
            self.root.update()
            from urllib.parse import quote
            encoded_name = quote(name, safe='')
            r = requests.post(f"{API_BASE}/media/{encoded_name}/return", timeout=3)
            if r.status_code == 200:
                self.status_label.config(text="🟢 Ready", foreground=self.success_color)
                messagebox.showinfo("✓ Returned", f"'{name}' has been returned")
                self.load_all()
            else:
                self.status_label.config(text="🔴 Return error", foreground=self.error_color)
                error_msg = r.json().get("error", r.text) if r.status_code != 500 else r.text
                messagebox.showerror("Error", f"Could not return: {error_msg}")
        except Exception as e:
            self.status_label.config(text="🔴 Error returning", foreground=self.error_color)
            messagebox.showerror("Error", f"Return failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
