import tkinter as tk
from PIL import Image, ImageTk  # Necesită instalarea Pillow: `pip install pillow`

class VirtualPet:
    def __init__(self, name):
        self.name = name
        self.hunger = 50
        self.energy = 50
        self.happiness = 50
        self.state = "idle"  # Starea curentă: idle, eat, sleep, etc.

    def feed(self):
        if self.hunger > 0:
            self.hunger = max(0, self.hunger - 10)
            self.happiness = min(100, self.happiness + 5)
            self.state = "eat"
            return f"L-ai hrănit pe {self.name}!"
        return f"{self.name} nu este flămând acum."

    def play(self):
        if self.energy > 10:
            self.happiness = min(100, self.happiness + 10)
            self.energy = max(0, self.energy - 15)
            self.hunger = min(100, self.hunger + 5)
            self.state = "idle"
            return f"Te-ai jucat cu {self.name}!"
        return f"{self.name} este prea obosit pentru a se juca."

    def sleep(self):
        if self.energy < 100:
            self.energy = min(100, self.energy + 20)
            self.hunger = min(100, self.hunger + 10)
            self.state = "sleep"
            return f"{self.name} a dormit și și-a refăcut energia!"
        return f"{self.name} nu are nevoie de somn acum."

    def get_status(self):
        return f"{self.name} - Foame: {self.hunger} | Energie: {self.energy} | Fericire: {self.happiness}"


class VirtualPetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet")
        self.root.geometry("500x600")

        # Dicționar pentru animații
        self.animations = {
            "idle": self.load_gif("Idle.gif"),
            "eat": self.load_gif("eat.gif"),
            "sleep": self.load_gif("sleep.gif"),
            "idle_to_sleep": self.load_gif("Idle_sleep.gif"),
            "sleep_to_idle": self.load_gif("sleep_idle.gif"),
            "pet": self.load_gif("pet.gif"),
        }

        self.pet = VirtualPet("Pisicuța Fluffy")

        # Etichetă pentru animație
        self.animation_label = tk.Label(root, bg="#a8d0e6")
        self.animation_label.pack(pady=20)

        # Etichetă cu statistici
        self.status_label = tk.Label(root, text=self.pet.get_status(), font=("Arial", 14), bg="#f8f1f1", bd=1, relief="solid")
        self.status_label.pack(pady=10)

        # Mesaj de acțiune
        self.message_label = tk.Label(root, text="", font=("Arial", 12), fg="green", bg="#f8f1f1")
        self.message_label.pack(pady=5)

        # Butoane pentru acțiuni
        self.feed_button = tk.Button(root, text="Hrănește", command=self.feed_pet, width=15, font=("Arial", 12), bg="#f76c6c", fg="white")
        self.feed_button.pack(pady=5)

        self.play_button = tk.Button(root, text="Joacă-te", command=self.play_pet, width=15, font=("Arial", 12), bg="#355c7d", fg="white")
        self.play_button.pack(pady=5)

        self.sleep_button = tk.Button(root, text="Dorm", command=self.sleep_pet, width=15, font=("Arial", 12), bg="#6c5b7b", fg="white")
        self.sleep_button.pack(pady=5)

        # Animația curentă
        self.current_animation = None
        self.animation_index = 0
        self.animation_timer = None

        # Redăm starea inițială
        self.play_animation("idle")
        self.update_status()

    def load_gif(self, file_path):
        """Încarcă toate cadrele unui GIF."""
        gif = Image.open(file_path)
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(len(frames))  # Treci la următorul cadru
        except EOFError:
            pass
        return frames

    def play_animation(self, animation_name, duration=5):
        """Redă animația specificată și revine la idle după durata specificată."""
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.animation_index = 0

        frames = self.animations[animation_name]
        if frames:
            frame = frames[self.animation_index]
            self.animation_label.config(image=frame)
            self.animation_index = (self.animation_index + 1) % len(frames)

            # Actualizare cadru o dată pe secundă
            self.animation_timer = self.root.after(1000, lambda: self.play_animation(animation_name, duration))

        # După durata specificată, revine la idle
        if self.animation_index == 0 and animation_name != "idle":
            self.root.after(duration * 1000, lambda: self.play_animation("idle"))

    def stop_animation(self):
        """Oprește animația curentă."""
        if self.animation_timer:
            self.root.after_cancel(self.animation_timer)

    def feed_pet(self):
        message = self.pet.feed()
        self.message_label.config(text=message, fg="green")
        self.stop_animation()
        self.play_animation("eat", duration=3)
        self.update_status()

    def play_pet(self):
        message = self.pet.play()
        self.message_label.config(text=message, fg="green")
        self.stop_animation()
        self.play_animation("pet", duration=3)
        self.update_status()

    def sleep_pet(self):
        message = self.pet.sleep()
        self.message_label.config(text=message, fg="green")
        self.stop_animation()
        self.play_animation("idle_to_sleep", duration=2)  # Tranziția durează 2 secunde
        self.play_animation("sleep", duration=6)  # După tranziție, redă somnul
        self.stop_animation()
        self.play_animation("sleep_to_idle", duration=5)  # Revine la idle după 5 secunde
        self.update_status()

    def update_status(self):
        self.status_label.config(text=self.pet.get_status())
        self.root.after(1000, self.pass_time)

    def pass_time(self):
        self.pet.hunger = min(100, self.pet.hunger + 1)
        self.pet.energy = max(0, self.pet.energy - 1)
        self.pet.happiness = max(0, self.pet.happiness - 1)
        self.update_status()


if __name__ == "__main__":
    root = tk.Tk()
    gui = VirtualPetGUI(root)
    root.mainloop()
