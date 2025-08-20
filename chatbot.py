import tkinter as tk
from tkinter import scrolledtext
import random

class CareerChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Career Guidance Chatbot")
        self.root.geometry("600x500")

        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED)
        self.chat_display.pack(pady=10)

        self.entry = tk.Entry(root, width=60)
        self.entry.pack(pady=5)

        self.send_button = tk.Button(root, text="Send", command=self.get_response)
        self.send_button.pack()

        self.responses = {
            "hello": ["Hello! How can I assist you?", "Hi there! What would you like to ask?"],
            "career": ["What field are you interested in?", "Tell me about your skills and interests."],
            "openness": ["You are creative and adaptable. Consider careers in design, writing, or research."],
            "conscientiousness": ["You are detail-oriented and reliable. Careers in finance, law, or engineering suit you."],
            "extroversion": ["You are sociable and energetic. Sales, marketing, or public relations may be a good fit."],
            "agreeableness": ["You are cooperative and empathetic. HR, counseling, or social work could be ideal."],
            "neuroticism": ["You are emotionally aware and analytical. Psychology, writing, or academia may work well."],
            "thankyou":["you are welcome.","Free to ask any guidences at anytime. bye."]
        }

        self.display_message("Chatbot", "Hello! I am your Career Guidance Chatbot. How can I help you today?")

    def display_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def get_response(self):
        user_input = self.entry.get().lower().strip()
        self.display_message("You", user_input)
        self.entry.delete(0, tk.END)

        response = self.generate_response(user_input)
        self.display_message("Chatbot", response)

    def generate_response(self, user_input):
        for keyword in self.responses:
            if keyword in user_input:
                return random.choice(self.responses[keyword])
        return "I'm not sure about that. Can you ask something else related to careers?"

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = CareerChatbot(root)
    root.mainloop()
