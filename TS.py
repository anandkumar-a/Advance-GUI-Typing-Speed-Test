import tkinter as tk
from tkinter import messagebox, Toplevel
import random
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import threading

text_samples = {
    "Easy": [
        "Many hands make light work.",
        "Strike while the iron is hot.",
        "Honesty is the best policy.",
        "The grass is always greener on the other side of the fence.",
        "Don't judge a book by its cover.",
        "An apple a day keeps the doctor away.",
        "Better late than never.",
        "Don't bite the hand that feeds you."
    ],
    "Medium": [
        "If you want something done right, you have to do it yourself.",
        "Keep your friends close and your enemies closer.",
        "Like father, like son.Like mother, like daughter.",
        "People who live in glass houses shouldn’t throw stones.",
        "You can lead a horse to the water, but you can’t make him drink it.",
        "When the going gets tough, the tough get going."
    ],
    "Hard": [
        "Actions are a true reflection of one’s intentions and character, whereas words can be empty or deceptive.",
        "It suggests that communication and intellectual influence are more effective and lasting than brute force.",
        "It reminds us that significant achievements and projects take time and effort. Patience and perseverance are crucial for achieving long-term goals.",
        "It suggests that one should look deeper to understand the true nature or value of something or someone.",
        "This proverb highlights the value of learning from experienced individuals. It can be used to discuss the importance of mentorship, cultural exchange, or traditional knowledge systems.",
        "This quote emphasises the transformative power of education. It can be used to discuss topics like poverty alleviation, women’s empowerment, or educational reforms.",
        " This quote connects justice with compassion and empathy. It can be used in essays about social justice, ethical leadership, or the role of government."
    ]
}

SCORE_FILE = "typing_scores.xlsx"

class TypingSpeedTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Test")
        self.master.geometry("850x600")
        self.master.configure(bg="#e8f0fe")

        self.username = ""
        self.level = tk.StringVar(value="Easy")
        self.text_to_type = ""
        self.session_results = []
        self.start_time = None
        self.sentences_to_use = []
        self.sentences_typed_count = 0

        self.show_registration_screen()

    def show_registration_screen(self):
        self.clear_widgets()

        tk.Label(self.master, text="Welcome to the Typing Challenge!", font=("Helvetica", 22, "bold"), bg="#e8f0fe", fg="#2c3e50").pack(pady=20)

        tk.Label(self.master, text="Enter Your Name:", font=("Helvetica", 14), bg="#e8f0fe", fg="#34495e").pack(pady=5)
        self.name_entry = tk.Entry(self.master, font=("Helvetica", 14), bg="#ffffff", fg="#2c3e50")
        self.name_entry.pack(pady=5)

        tk.Label(self.master, text="Select Difficulty:", font=("Helvetica", 14), bg="#e8f0fe", fg="#34495e").pack(pady=10)
        tk.OptionMenu(self.master, self.level, *text_samples.keys()).pack(pady=5)

        tk.Button(self.master, text="Start Test", command=self.start_test,
                  font=("Helvetica", 14, "bold"), bg="#1abc9c", fg="white", padx=10, pady=5).pack(pady=20)

    def start_test(self):
        self.username = self.name_entry.get().strip() or "Anonymous"
        self.session_results.clear()
        self.sentences_typed_count = 0
        self.sentences_to_use = random.sample(text_samples[self.level.get()], len(text_samples[self.level.get()]))
        self.show_test_screen()

    def show_test_screen(self):
        self.clear_widgets()
        if self.sentences_typed_count < len(self.sentences_to_use):
            self.text_to_type = self.sentences_to_use[self.sentences_typed_count]
            self.start_time = time.time()
            self.sentences_typed_count += 1
            
            tk.Label(self.master, text=f"Typing Test - {self.level.get()} Level", font=("Helvetica", 18, "bold"), bg="#e8f0fe", fg="#2c3e50").pack(pady=10)

            self.text_display = tk.Text(self.master, height=6, width=90, font=("Helvetica", 16), wrap=tk.WORD, bd=2, relief=tk.RIDGE, bg="#fdfefe", fg="#2c3e50", state="disabled")
            self.text_display.pack(pady=15)
            self.display_text_with_colors(self.text_to_type, "")

            self.entry = tk.Text(self.master, height=6, width=90, font=("Helvetica", 14), wrap=tk.WORD, bd=2, relief=tk.SUNKEN, bg="#ffffff", fg="#2c3e50")
            self.entry.pack(pady=10)
            self.entry.bind("<KeyRelease>", self.update_live_feedback)

            self.result_label = tk.Label(self.master, text="", font=("Helvetica", 14), bg="#e8f0fe", fg="green")
            self.result_label.pack(pady=10)

            btn_frame = tk.Frame(self.master, bg="#e8f0fe")
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="Next", command=self.next_sentence,
                      font=("Helvetica", 14), bg="#28a745", fg="white", padx=10, pady=5).grid(row=0, column=0, padx=5)

            tk.Button(btn_frame, text="Summary", command=self.show_summary,
                      font=("Helvetica", 14), bg="#f39c12", fg="white", padx=10, pady=5).grid(row=0, column=1, padx=5)

            tk.Button(btn_frame, text="Restart", command=self.show_registration_screen,
                      font=("Helvetica", 14), bg="#007acc", fg="white", padx=10, pady=5).grid(row=0, column=2, padx=5)

            tk.Button(btn_frame, text="View Leaderboard", command=self.show_full_leaderboard,
                      font=("Helvetica", 12), bg="#2980b9", fg="white", padx=10, pady=5).grid(row=0, column=3, padx=5)
            
            tk.Button(btn_frame, text="Show Progress Graph", command=self.show_progress_graph,
                      font=("Helvetica", 12), bg="#673ab7", fg="white", padx=10, pady=5).grid(row=0, column=4, padx=5)

        else:
            self.clear_widgets()
            tk.Label(self.master, text="THE END, YOU CAN LEAVE", font=("Helvetica", 22, "bold"), bg="#e8f0fe", fg="#2c3e50").pack(pady=50)
            
            btn_frame = tk.Frame(self.master, bg="#e8f0fe")
            btn_frame.pack(pady=10)
            
            tk.Button(btn_frame, text="Summary", command=self.show_summary,
                      font=("Helvetica", 14), bg="#f39c12", fg="white", padx=10, pady=5).grid(row=0, column=0, padx=5)
            
            tk.Button(btn_frame, text="Restart", command=self.show_registration_screen,
                      font=("Helvetica", 14), bg="#007acc", fg="white", padx=10, pady=5).grid(row=0, column=1, padx=5)

    def update_live_feedback(self, event=None):
        typed_text = self.entry.get("1.0", tk.END).strip()
        original = self.text_to_type.strip()
        
        # Calculate and display live metrics
        elapsed = time.time() - self.start_time
        word_count = len(typed_text.split())
        wpm = (word_count / elapsed) * 60 if elapsed > 0 else 0
        
        correct_chars = sum(1 for i in range(min(len(original), len(typed_text))) if original[i] == typed_text[i])
        accuracy = (correct_chars / len(original)) * 100 if original else 0
        
        self.result_label.config(text=f"Live WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")

        # Visual highlighting
        self.display_text_with_colors(original, typed_text)

    def display_text_with_colors(self, original, typed):
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        
        self.text_display.tag_configure("correct", foreground="green")
        self.text_display.tag_configure("incorrect", foreground="red")
        
        for i, char in enumerate(original):
            if i < len(typed):
                if typed[i] == char:
                    self.text_display.insert(tk.END, char, "correct")
                else:
                    self.text_display.insert(tk.END, char, "incorrect")
            else:
                self.text_display.insert(tk.END, char)
        
        self.text_display.config(state="disabled")

    def next_sentence(self):
        typed_text = self.entry.get("1.0", tk.END).strip()
        original = self.text_to_type.strip()
        elapsed = time.time() - self.start_time

        correct_chars = sum(1 for i in range(min(len(original), len(typed_text))) if original[i] == typed_text[i])
        char_accuracy = (correct_chars / len(original)) * 100 if original else 0
        wpm = (len(typed_text.split()) / elapsed) * 60 if elapsed > 0 else 0

        self.session_results.append((wpm, char_accuracy, elapsed))

        self.save_score_to_excel(self.username, char_accuracy, wpm, elapsed)

        self.show_test_screen()

    def save_score_to_excel(self, name, accuracy, wpm, time_taken):
        try:
            if os.path.exists(SCORE_FILE):
                df = pd.read_excel(SCORE_FILE)
            else:
                df = pd.DataFrame(columns=["Timestamp", "Name", "Accuracy (%)", "WPM", "Time Taken (seconds)"])

            new_score = pd.DataFrame({
                "Timestamp": [pd.Timestamp.now()],
                "Name": [name],
                "Accuracy (%)": [round(accuracy, 2)],
                "WPM": [round(wpm, 2)],
                "Time Taken (seconds)": [round(time_taken, 2)]
            })

            df = pd.concat([df, new_score], ignore_index=True)
            df.to_excel(SCORE_FILE, index=False)
            print(f"Score for {name} saved successfully to {SCORE_FILE}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save score to Excel file: {e}")

    def show_summary(self):
        if not self.session_results:
            messagebox.showinfo("Summary", "No test results to summarize.")
            return

        avg_wpm = sum(res[0] for res in self.session_results) / len(self.session_results)
        avg_accuracy = sum(res[1] for res in self.session_results) / len(self.session_results)
        total_time = sum(res[2] for res in self.session_results)

        summary_text = (
            f"Session Summary for {self.username}:\n\n"
            f"Average WPM: {avg_wpm:.2f}\n"
            f"Average Accuracy: {avg_accuracy:.2f}%\n"
            f"Total time for sentences: {total_time:.2f} seconds"
        )
        messagebox.showinfo("Summary", summary_text)

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def show_full_leaderboard(self):
        if not os.path.exists(SCORE_FILE):
            messagebox.showinfo("Leaderboard", "No scores to display.")
            return

        top = Toplevel(self.master)
        top.title("Full Leaderboard")
        top.geometry("600x600")
        top.configure(bg="#ecf0f1")

        tk.Label(top, text="Full Leaderboard", font=("Helvetica", 16, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)

        try:
            df = pd.read_excel(SCORE_FILE)
            if df.empty:
                messagebox.showinfo("Leaderboard", "No scores to display.")
                top.destroy()
                return

            df = df.sort_values(by="Accuracy (%)", ascending=False)
            leaderboard_text = "\n".join([f"{i+1}. {row['Name']} — {row['Accuracy (%)']:.2f}% Accuracy | {row['Time Taken (seconds)']:.2f}s | {row['WPM']:.2f} WPM" for i, row in df.iterrows()])
            tk.Label(top, text=leaderboard_text, font=("Helvetica", 12), justify="left", bg="#ecf0f1", fg="#34495e").pack(pady=5, padx=10, anchor='w')

        except Exception as e:
            messagebox.showerror("Error", f"Could not load leaderboard from Excel file: {e}")
            top.destroy()
    
    def show_progress_graph(self):
        # Run plotting in a separate thread to prevent GUI from freezing
        threading.Thread(target=self._plot_graph_thread).start()

    def _plot_graph_thread(self):
        try:
            if not os.path.exists(SCORE_FILE):
                messagebox.showinfo("Progress Graph", "No data to display a graph.")
                return
            
            df = pd.read_excel(SCORE_FILE)
            user_data = df[df['Name'] == self.username].copy()
            
            if user_data.empty:
                messagebox.showinfo("Progress Graph", "No data for this user to display a graph.")
                return

            user_data['Timestamp'] = pd.to_datetime(user_data['Timestamp'])

            plt.style.use('seaborn-v0_8-whitegrid')
            fig, ax = plt.subplots(figsize=(10, 6))

            ax.plot(user_data['Timestamp'], user_data['WPM'], marker='o', linestyle='-', color='#1abc9c', label='WPM')
            ax.set_title(f'WPM Progress for {self.username}', fontsize=16)
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Words Per Minute (WPM)', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.legend()
            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Could not generate graph: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
