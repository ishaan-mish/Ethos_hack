# dataset_loader.py
import pandas as pd
import re

class DatasetLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load(self):
        # Load CSV
        try:
            self.data = pd.read_csv(self.file_path)
        except Exception as e:
            raise ValueError(f"Error loading dataset: {e}")

        # Validate required columns
        required_cols = [
            "topic", "problem_statement", "solution",
            "answer_option_1", "answer_option_2", "answer_option_3",
            "answer_option_4", "answer_option_5", "correct_option_number"
        ]
        for col in required_cols:
            if col not in self.data.columns:
                raise ValueError(f"Missing required column: {col}")

        # Clean and normalize
        self._clean_data()

        # Return as structured list of dicts
        return self.data.to_dict(orient="records")

    def _clean_data(self):
        # Normalize text fields
        text_cols = [
            "topic", "problem_statement", "solution",
            "answer_option_1", "answer_option_2", "answer_option_3",
            "answer_option_4", "answer_option_5"
        ]
        for col in text_cols:
            self.data[col] = self.data[col].apply(self._normalize_text)

        # Convert correct option to integer
        self.data["correct_option_number"] = self.data["correct_option_number"].astype(int)

    def _normalize_text(self, text):
        if pd.isna(text):
            return ""
        text = str(text).strip().lower()
        text = re.sub(r"[^a-z0-9\s\.\,\?\!\(\)\+\-\*/=<>]", "", text)
        return text
