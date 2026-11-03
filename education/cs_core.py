"""
CSE Aspirant - Computer Science Core Subjects (Hindi & English)
"""
from typing import Dict, Any

class ComputerScienceCore:
    def __init__(self):
        self.subjects = {
            "os": {
                "title_en": "Operating Systems",
                "title_hi": "ऑपरेटिंग सिस्टम्स",
                "content_en": "Process Scheduling, Deadlocks, Memory Management, Paging, Virtual Memory, Inode File Systems.",
                "content_hi": "प्रक्रिया निर्धारण (Scheduling), डेडलॉक, मेमोरी प्रबंधन, पेजिंग, वर्चुअल मेमोरी और फाइल सिस्टम।"
            },
            "dbms": {
                "title_en": "Database Management Systems",
                "title_hi": "डेटाबेस मैनेजमेंट सिस्टम",
                "content_en": "ACID Properties, Normalization (1NF to BCNF), Relational Algebra, SQL, Indexing (B+ Trees), Concurrency Control.",
                "content_hi": "ACID गुण, नॉर्मलाइजेशन (1NF से BCNF), रिलेशनल अल्जेब्रा, इंडेक्सिंग (B+ ट्री) और कॉनकरेंसी कंट्रोल।"
            },
            "cn": {
                "title_en": "Computer Networks",
                "title_hi": "कंप्यूटर नेटवर्क्स",
                "content_en": "OSI & TCP/IP Models, Flow Control, Congestion Control, Routing Algorithms (Dijkstra, Bellman-Ford), DNS, HTTPS.",
                "content_hi": "OSI और TCP/IP मॉडल, फ्लो कंट्रोल, कंजेशन कंट्रोल, रूटिंग एल्गोरिदम (Dijkstra, Bellman-Ford) और सुरक्षा।"
            },
            "dsa": {
                "title_en": "Data Structures & Algorithms",
                "title_hi": "डेटा स्ट्रक्चर्स और एल्गोरिदम",
                "content_en": "Arrays, Linked Lists, Trees, Graphs, Dynamic Programming, Greedy Algorithms, Asymptotic Time & Space Complexities.",
                "content_hi": "ऐरे, लिंक्ड लिस्ट, ट्री, ग्राफ, डायनेमिक प्रोग्रामिंग, लालची एल्गोरिदम और समय-स्थान जटिलता।"
            }
        }

    def get_subject_overview(self, subject: str, lang: str = "en") -> str:
        lang = "hi" if lang.lower() == "hi" else "en"
        data = self.subjects.get(subject.lower(), self.subjects["os"])
        title = data[f"title_{lang}"]
        content = data[f"content_{lang}"]
        return f"📚 **{title}**:\n{content}"

cs_core = ComputerScienceCore()
