import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pathlib import Path
import shutil

class ImagePickerApp:
    def __init__(self, root, data):
        self.root = root
        self.root.title("TrendWave & SpaceMind - Fixed Layout Picker")
        
        # Force a fixed window size so it doesn't jump around
        self.root.geometry("900x950")
        self.root.resizable(False, False)
        
        self.data = data
        self.scenes = data.get('scenes', [])
        self.current_scene_idx = 0
        self.current_image_idx = 0
        self.fetch_dir = Path("images/fetched")
        
        self.setup_ui()
        self.load_scene()

    def setup_ui(self):
        # 1. NAVIGATION BAR (Moved to TOP so it never disappears)
        self.nav_frame = ttk.Frame(self.root, padding="10", relief="raised")
        self.nav_frame.pack(fill="x", side="top")

        self.btn_prev = ttk.Button(self.nav_frame, text="<< PREV IMAGE", command=self.prev_image)
        self.btn_prev.pack(side="left", padx=20)

        self.btn_select = ttk.Button(self.nav_frame, text="✅ SELECT & NEXT SCENE", 
                                     command=self.select_winner, cursor="hand2")
        self.btn_select.pack(side="left", expand=True)

        self.btn_next = ttk.Button(self.nav_frame, text="NEXT IMAGE >>", command=self.next_image)
        self.btn_next.pack(side="right", padx=20)

        # 2. SCRIPT INFO SECTION
        self.info_frame = ttk.Frame(self.root, padding="10")
        self.info_frame.pack(fill="x")
        
        self.progress_label = ttk.Label(self.info_frame, text="", font=("Arial", 14, "bold"))
        self.progress_label.pack()
        
        self.text_display = tk.Text(self.info_frame, height=3, font=("Arial", 11), 
                                    wrap="word", bg="#f4f4f4", state="disabled")
        self.text_display.pack(fill="x", pady=5)

        # 3. IMAGE DISPLAY AREA (Fixed size container)
        self.img_container = ttk.Frame(self.root, width=850, height=700)
        self.img_container.pack_propagate(False) # Prevents frame from shrinking
        self.img_container.pack(pady=10)
        
        self.img_label = ttk.Label(self.img_container)
        self.img_label.pack(expand=True)

    def load_scene(self):
        if self.current_scene_idx >= len(self.scenes):
            messagebox.showinfo("Done", "Selections complete! Closing...")
            self.root.destroy()
            return

        scene = self.scenes[self.current_scene_idx]
        self.progress_label.config(text=f"SCENE {self.current_scene_idx + 1} OF {len(self.scenes)}")
        
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, f"{scene['headline'].lower()}\n{scene['details'].lower()}")
        self.text_display.config(state="disabled")
        
        self.current_image_idx = 0
        self.show_image()

    def get_available_images(self):
        scene_dir = self.fetch_dir / f"scene_{self.current_scene_idx}"
        image_list = []
        if scene_dir.exists():
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.jfif']:
                image_list.extend(list(scene_dir.glob(ext)))
                image_list.extend(list(scene_dir.glob(ext.upper())))
        return sorted(list(set(image_list)))

    def show_image(self):
        imgs = self.get_available_images()
        if not imgs:
            self.img_label.config(image='', text="No images found for this scene!")
            return

        img_path = imgs[self.current_image_idx % len(imgs)]
        try:
            img = Image.open(img_path)
            # FORCE RE-SIZE to fit the container precisely
            img.thumbnail((800, 650))
            self.tk_img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.tk_img, text="")
            self.current_img_path = img_path
        except Exception as e:
            self.img_label.config(text=f"Error: {e}")

    def next_image(self):
        self.current_image_idx += 1
        self.show_image()

    def prev_image(self):
        self.current_image_idx -= 1
        self.show_image()

    def select_winner(self):
        if hasattr(self, 'current_img_path'):
            target = self.fetch_dir / f"{self.current_scene_idx}.jpg"
            shutil.copy(self.current_img_path, target)
            print(f"DEBUG: Saved {self.current_img_path.name} as {target.name}")
            self.current_scene_idx += 1
            self.load_scene()

if __name__ == "__main__":
    with open("data.json", "r", encoding='utf-8-sig') as f:
        data = json.load(f)
    root = tk.Tk()
    app = ImagePickerApp(root, data)
    root.mainloop()