import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random

class VirtualPet:
    def __init__(self, name):
        self.name = name
        self.hunger = 50
        self.energy = 50
        self.happiness = 50
        self.state = "idle"

    def feed(self):
        if self.hunger > 0:
            self.hunger = max(0, self.hunger - 10)
            self.happiness = min(100, self.happiness + 5)
            self.state = "eat"
            return f"You fed {self.name}!"
        return f"{self.name} is not hungry anymore."

    def play(self):
        if self.energy > 10:
            self.happiness = min(100, self.happiness + 10)
            self.energy = max(0, self.energy - 15)
            self.hunger = min(100, self.hunger + 5)
            self.state = "idle"
            return f"You pet {self.name}!"
        return f"{self.name} is too tired."

    def sleep(self):
        if self.energy < 95:
            self.energy = min(100, self.energy + 20)
            self.hunger = min(100, self.hunger + 10)
            self.state = "sleep"
            return f"{self.name} is sleeping."
        return f"{self.name} doesn't need sleep."

    def change_name(self, new_name):
        self.name = new_name
        return f"The name has been changed to {self.name}!"

    def get_status(self):
        return f"Hunger: {self.hunger}\nEnergy: {self.energy}\nHappiness: {self.happiness}"

    def update_pet_status(self):
        self.hunger = min(100, self.hunger + 1)
        self.energy = max(0, self.energy - 1)
        self.happiness = max(0, self.happiness - 1)


class VirtualPetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet")
        self.root.geometry("600x400")
        self.root.config(bg='black')

        self.pet = VirtualPet("Fluffy")

        # Numele pisicii
        self.name_label = tk.Label(self.root, text=self.pet.name, font=("8514oem Regular", 20, "bold"), bg='black', fg="white")
        self.name_label.pack(pady=10)

        # Cadru principal
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Cadru pentru butoane
        self.button_frame = tk.Frame(self.main_frame, bg='black')
        self.button_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        self.feed_button = tk.Button(self.button_frame, text="FEED", command=self.feed_pet, font=("8514oem Regular", 10), width=12, bg="#f76c6c", fg="white")
        self.feed_button.pack(pady=5)

        self.play_button = tk.Button(self.button_frame, text="PET", command=self.play_pet, font=("8514oem Regular", 10), width=12, bg="#355c7d", fg="white")
        self.play_button.pack(pady=5)

        self.sleep_button = tk.Button(self.button_frame, text="SLEEP", command=self.sleep_pet, font=("8514oem Regular", 10), width=12, bg="#6c5b7b", fg="white")
        self.sleep_button.pack(pady=5)

        self.change_name_button = tk.Button(self.button_frame, text="CHANGE NAME", command=self.change_name, font=("8514oem Regular", 10), width=12, bg="#8e44ad", fg="white")
        self.change_name_button.pack(pady=5)

        self.message_label = tk.Label(self.main_frame, text="", font=("8514oem Regular", 14), bg='black', fg="white",
                                      justify=tk.CENTER)
        self.message_label.pack(side=tk.BOTTOM, padx=10, pady=5, anchor=tk.CENTER)

        # Etichetă pentru animație
        self.animation_label = tk.Label(self.main_frame, bg='black')
        self.animation_label.pack(side=tk.LEFT, expand=True)

        # Statusurile pisicii
        self.status_label = tk.Label(self.main_frame, text=self.pet.get_status(), font=("8514oem Regular", 14), bg='black', fg="white", justify=tk.LEFT)
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=10)

        # Animația curentă
        self.current_animation = None
        self.animation_index = 0
        self.animation_timer = None

        # Încarcă animațiile
        self.animations = {
            "idle": self.load_gif("Idle.gif"),
            "eat": self.load_gif("eat.gif"),
            "sleep": self.load_gif("sleep.gif"),
            "pet": self.load_gif("pet.gif")
        }

        self.play_animation("idle")
        self.update_status()

    def load_gif(self, file_path, scale=(300, 300)):
        gif = Image.open(file_path)
        frames = []
        try:
            while True:
                frame = gif.copy()
                frame = frame.convert("RGBA")  # Convertim în format RGBA pentru transparență
                frame = frame.resize(scale, Image.Resampling.LANCZOS)
                transparent = Image.new("RGBA", frame.size, (0, 0, 0, 0))  # Fundal transparent
                transparent.paste(frame, mask=frame.split()[3])  # Aplicăm transparența
                frames.append(ImageTk.PhotoImage(transparent))
                gif.seek(len(frames))  # Treci la următorul cadru
        except EOFError:
            pass
        return frames

    def play_animation(self, animation_name, loop=False, loop_count=1, duration=None):
        frames = self.animations[animation_name]
        if not hasattr(self, 'current_loop_count'):
            self.current_loop_count = 0

        if frames:
            frame = frames[self.animation_index]
            self.animation_label.config(image=frame)
            self.animation_index = (self.animation_index + 1) % len(frames)

            if self.animation_index == 0 and not loop:
                self.current_loop_count += 1

            if loop or (self.current_loop_count < loop_count):
                self.animation_timer = self.root.after(500,
                                                       lambda: self.play_animation(animation_name, loop, loop_count,
                                                                                   duration))
            else:
                self.current_loop_count = 0
                if duration:
                    self.root.after(duration, lambda: self.play_animation("idle", loop=True))
                else:
                    self.play_animation("idle", loop=True)

    def feed_pet(self):
        message = self.pet.feed()
        self.message_label.config(text=message)
        if message == f"{self.pet.name} is not hungry anymore.":
            return
        self.stop_animation()
        self.animation_index = 0
        self.play_animation("eat", loop=False, duration=100)

    def play_pet(self):
        message = self.pet.play()
        self.message_label.config(text=message)
        if message == f"{self.pet.name} is too tired.":
            return
        self.stop_animation()
        self.animation_index = 0
        self.play_animation("pet", loop=False, duration=100)

    def sleep_pet(self):
        message = self.pet.sleep()
        self.message_label.config(text=message)
        if message == f"{self.pet.name} doesn't need sleep.":
            return
        self.stop_animation()
        self.animation_index = 0
        self.play_animation("sleep", loop=False, loop_count=3, duration=None)

    def change_name(self):
        def submit_name():
            new_name = name_entry.get()
            if new_name.strip():
                if len(new_name) > 6:
                    self.pet.energy = min(100, self.pet.energy - 4)
                    self.message_label.config(text=f"The name is too confusing for {self.pet.name}! Try another.")
                    popup.destroy()
                    self.change_name()
                elif random.randint(1, 100) <= 30:  # 30% șansă să nu-i placă
                    self.pet.happiness = min(100, self.pet.happiness - 4)
                    self.message_label.config(text=f"{self.pet.name} doesn't like this name! Try another.")
                    popup.destroy()
                    self.change_name()
                else:
                    message = self.pet.change_name(new_name)
                    self.pet.happiness = min(100, self.pet.happiness + 7)
                    self.name_label.config(text=self.pet.name)
                    self.message_label.config(text=message)
                    self.play_animation("pet", loop=False, loop_count=2, duration=200)
                    popup.destroy()
            else:
                self.message_label.config(text="Name cannot be empty!")

        popup = tk.Toplevel(self.root)
        popup.title("Change Name")
        popup.geometry("300x150")
        popup.config(bg='black')

        tk.Label(popup, text="Enter new name:", font=("8514oem Regular", 12), bg='black', fg="white").pack(pady=10)
        name_entry = tk.Entry(popup, font=("8514oem Regular", 12))
        name_entry.pack(pady=5)

        submit_button = tk.Button(popup, text="Submit", command=submit_name, font=("8514oem Regular", 10), bg="#27ae60",
                                  fg="white")
        submit_button.pack(pady=10)

    def stop_animation(self):
        if self.animation_timer:
            self.root.after_cancel(self.animation_timer)
        self.animation_timer = None

    def update_status(self):
        self.pet.update_pet_status()
        self.status_label.config(text=self.pet.get_status())
        self.root.after(2000, self.update_status)


if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualPetGUI(root)
    root.mainloop()
