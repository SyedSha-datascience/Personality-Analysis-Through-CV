import tkinter as tk
from tkinter import Label
from tkinter import filedialog, messagebox
import PyPDF2
import docx
import os
import pickle
import subprocess
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from collections import Counter
COMPANY_NAME="SHARPVIEW RECURRING'S"

# Download necessary NLTK data
nltk.download('punkt')

class PersonalityPredictor:
    def __init__(self, root):
        self.root = root
        self.root.title("Personality Prediction via CV Analysis")
        self.root.geometry("800x600")

        # UI Components
        Label(root, text=f"Company: {COMPANY_NAME}", font=("Arial",14,"bold")).pack(pady=10)
        
        
        self.label = tk.Label(root, text="Upload CV (PDF/DOCX)", font=("Arial", 12))
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_cv)
        self.upload_button.pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 10), wraplength=700)
        self.result_label.pack(pady=10)

        self.history_button = tk.Button(root, text="Show Past Results", command=self.show_results)
        self.history_button.pack(pady=5)

        self.compare_button = tk.Button(root, text="Compare Two CVs", command=self.compare_resumes)
        self.compare_button.pack(pady=5)

        self.rank_button = tk.Button(root, text="Rank Resumes", command=self.rank_resumes)
        self.rank_button.pack(pady=10)

        self.interview_button=tk.Button(root, text="Generate Interview Questions",command=self.generate_interview_questions)
        self.interview_button.pack(pady=10)

        self.chatbot_button = tk.Button(root, text="Career Guidance Chatbot", command=self.open_chatbot)
        self.chatbot_button.pack(pady=5)

        # Preload TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')
        sample_text = ["sample text for tfidf vectorization"]
        self.vectorizer.fit(sample_text)

        # Define random personality weights
        feature_size = len(self.vectorizer.get_feature_names_out())
        self.weights = {trait: np.random.rand(feature_size) for trait in 
                        ["Openness", "Conscientiousness", "Extroversion", "Agreeableness", "Neuroticism"]}

        # Career Guidance Knowledge Base
        self.career_knowledge = {
            "Openness": "You are creative and adaptable. Careers in design, writing, or research suit you.",
            "Conscientiousness": "You are detail-oriented and reliable. Consider finance, law, or engineering.",
            "Extroversion": "You are sociable and energetic. Sales, marketing, or public relations may fit you.",
            "Agreeableness": "You are cooperative and empathetic. HR, counseling, or social work may be ideal.",
            "Neuroticism": "You are emotionally aware and analytical. Psychology, writing, or academia may work well."
        }

    def open_chatbot(self):
        try:
            subprocess.Popen(["python","chatbot.py"])

        except FileNotFoundError:
            messagebox.showerror("Error:","chatbot script not found!")

    def upload_cv(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
        if file_path:
            text = self.extract_text(file_path)
            if not text.strip():
                messagebox.showerror("Error", "The selected file is empty or unreadable.")
                return

            personality = self.predict_personality(text)
            feedback = self.provide_feedback(personality)
            career_suggestions = self.recommend_career(personality)
            interview_questions = self.generate_interview_questions(text)

            candidate_name = os.path.basename(file_path).split('.')[0]
            self.save_result(candidate_name, personality)

            result_text = (f"Predicted Personality: {personality}\n\n"
                           f"Feedback: {feedback}\n\n"
                           f"Suggested Careers: {career_suggestions}\n\n")

            self.result_label.config(text=result_text)

    def extract_text(self, file_path):
        text = ""
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + " "
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "
        return text.lower().strip()

    def predict_personality(self, text):
        words = word_tokenize(text)
        word_vectors = self.vectorizer.transform([" ".join(words)]).toarray()
        scores = {trait: word_vectors.dot(self.weights[trait].T)[0] for trait in self.weights}
        return max(scores, key=scores.get)

    def provide_feedback(self, personality):
        return self.career_knowledge.get(personality, "Your personality analysis is unique.")

    def recommend_career(self, personality):
        return self.career_knowledge.get(personality, "No specific career match found.")

    def generate_interview_questions(self, text="Default text"):
        if not hasattr(self, 'skills') or not self.skills:
            questions = ["Tell me about yourself.", "What are your strengths and weaknesses?", "Where do you see yourself in five years?"]
        else:
            questions = [f"Can you explain your experience with {skill}?" for skill in self.skills]
            questions += [f"How have you applied {skill} in real-world projects?" for skill in self.skills]
        
        question_text = "\n".join(questions)
        messagebox.showinfo("Interview Questions", question_text)

    def compare_resumes(self):
        file1 = filedialog.askopenfilename(title="Select First CV")
        file2 = filedialog.askopenfilename(title="Select Second CV")
        if file1 and file2:
            personality1 = self.predict_personality(self.extract_text(file1))
            personality2 = self.predict_personality(self.extract_text(file2))
            comparison_result = f"CV1: {personality1}\nCV2: {personality2}"
            messagebox.showinfo("Comparison Result", comparison_result)

    def rank_resumes(self):
        job_description = filedialog.askopenfilename(title="Select Job Description (TXT)")
        if not job_description:
            return
        with open(job_description, "r", encoding="latin-1") as file:
            job_text = file.read().lower()
        resumes = []
        file_paths = filedialog.askopenfilenames(title="Select CVs to Rank")
        for file_path in file_paths:
            resumes.append(self.extract_text(file_path))

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([job_text] + resumes)
        scores = (tfidf_matrix[0] @ tfidf_matrix[1:].T).toarray()[0]

        ranking = sorted(zip(file_paths, scores), key=lambda x: x[1], reverse=True)
        result_text = "\n".join([f"{os.path.basename(r[0])}: {round(r[1], 2)}" for r in ranking])
        messagebox.showinfo("Resume Ranking", f"Resumes ranked for {COMPANY_NAME}. Check results! \n\n{result_text}")

    def save_result(self, name, personality):
        with open("personality_results.pkl", "ab") as file:
            pickle.dump({"name": name, "personality": personality}, file)

    def load_results(self):
        results = []
        try:
            with open("personality_results.pkl", "rb") as file:
                while True:
                    try:
                        results.append(pickle.load(file))
                    except EOFError:
                        break
        except (FileNotFoundError, pickle.UnpicklingError):
            return []
        return results

    def show_results(self):
        results = self.load_results()
        if not results:
            messagebox.showinfo("Past Results", "No past results found.")
            return
        result_text = "\n".join([f"{r['name']}: {r['personality']}" for r in results])
        messagebox.showinfo("Past Results", result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalityPredictor(root)
    root.mainloop()
