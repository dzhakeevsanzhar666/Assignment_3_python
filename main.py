import os
import csv
import json

class FileManager:
    # Task 1: File Manager
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        print(f"Error: {self.filename} not found.")
        return False

    def create_output_folder(self, folder='output'):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")

class DataLoader:
    # Task 2: Data Loader
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.students = list(reader)
            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students
        except Exception as e:
            print(f"Error loading data: {e}")
            return []

    def preview(self, n=5):
        print(f"\nFirst {n} rows:")
        print("-" * 30)
        for s in self.students[:n]:
            print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")
        print("-" * 30)

class DataAnalyser:
    # Task 3: Data Analyser
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        gpas = []
        # Сначала собираем все валидные GPA в список
        for s in self.students:
            try:
                gpa_val = float(s['GPA'])
                gpas.append(gpa_val)
            except ValueError:
                continue
        
        high_students = list(filter(lambda x: float(x['GPA']) > 3.5, self.students))
        high_performers = len(high_students)

        if gpas:
            self.result = {
                "analysis": "GPA Statistics",
                "total_students": len(self.students),
                "average_gpa": round(sum(gpas) / len(gpas), 2),
                "max_gpa": max(gpas),
                "min_gpa": min(gpas),
                "high_performers": high_performers
            }
        return self.result

    def print_results(self):
        if not self.result: 
            print("No results to print.")
            return
        print("\nGPA Analysis\n" + "-" * 30)
        print(f"Total students   : {self.result['total_students']}")
        print(f"Average GPA      : {self.result['average_gpa']}")
        print(f"Highest GPA      : {self.result['max_gpa']}")
        print(f"Lowest GPA       : {self.result['min_gpa']}")
        print(f"Students GPA>3.5 : {self.result['high_performers']}")

class ResultSaver:
    # Task 4: Result Saver
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.result, f, indent=4)
            print(f"\nResult saved to {self.output_path}")
        except Exception as e:
            print(f"Error saving JSON: {e}")

if __name__ == "__main__":
    # Task 5: Main Integration
    FILE = 'global_university_students_performance_habits_10000.csv'
    
    fm = FileManager(FILE)
    if fm.check_file():
        fm.create_output_folder()
        
        dl = DataLoader(FILE)
        data = dl.load()
        
        if data:
            dl.preview(5)
            
            analyser = DataAnalyser(data)
            analyser.analyse()
            analyser.print_results()
            
            saver = ResultSaver(analyser.result, 'output/result.json')
            saver.save_json()
