"""
CSE Aspirant - Books and Notes Library
"""
from typing import List, Dict

class NotesLibrary:
    def __init__(self):
        self.library = [
            {"title": "Indian Polity by M. Laxmikanth (7th Edition)", "category": "Polity", "lang": "Dual (EN/HI)", "url": "https://cse-aspirant.org/books/polity"},
            {"title": "Operating System Concepts (Silberschatz)", "category": "Computer Science", "lang": "EN", "url": "https://cse-aspirant.org/books/os"},
            {"title": "A Brief History of Modern India (Spectrum)", "category": "History", "lang": "Dual (EN/HI)", "url": "https://cse-aspirant.org/books/spectrum"},
            {"title": "Introduction to Algorithms (CLRS 4th Edition)", "category": "DSA", "lang": "EN", "url": "https://cse-aspirant.org/books/clrs"},
            {"title": "Indian Economy by Nitin Singhania / Ramesh Singh", "category": "Economy", "lang": "Dual (EN/HI)", "url": "https://cse-aspirant.org/books/economy"}
        ]

    def list_books(self, category: str = "") -> List[Dict[str, str]]:
        if not category:
            return self.library
        return [b for b in self.library if b["category"].lower() == category.lower()]

notes_library = NotesLibrary()
