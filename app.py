from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

# Result links from your original code
results_links = {
    "1_1": [
        "https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-JULY-2021.php",
        "https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-DEC-2021.php",
        "https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-MARCH-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-JULY-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-FEB-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-JULY-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-JAN-2024.php",
        "https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-JUNE-2024.php",
        "https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-DEC-2024.php",
    ],
    "1_2": [
        "https://www.nriitexamcell.com/autonomous/results/1-2-NRIA20-SEPT-2021.php",
        "https://www.nriitexamcell.com/autonomous/results/1-2-NRIA20-APRIL-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/1-2-NRIA20-JULY-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/1-2-NRIA20-JAN-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/1-2-NRIA20-JUNE-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/1-2-NRIA20-JAN-2024.php",
        "https://www.nriitexamcell.com/autonomous/results/1-2-NRIA20-JUNE-2024.php",
        "https://www.nriitexamcell.com/autonomous/results/1-2-NRIA20-DEC-2024.php",
    ],
    "2_1": [
        "https://www.nriitexamcell.com/autonomous/results/2-1-NRIA20-FEB-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/2-1-NRIA20-JUNE-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/2-1-NRIA20-DEC-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/2-1-NRIA20-JUNE-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/2-1-NRIA20-DEC-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/2-1-NRIA20-JUNE-2024.php",
        "https://www.nriitexamcell.com/autonomous/results/2-1-NRIA20-NOV-2024.php",
    ],
    "2_2": [
        "https://www.nriitexamcell.com/autonomous/results/2-2-NRIA20-MAY-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/2-2-NRIA20-NOV-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/2-2-NRIA20-MAY-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/2-2-NRIA20-DEC-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/2-2-NRIA20-MAY-2024.php",
        "https://www.nriitexamcell.com/autonomous/results/2-2-NRIA20-NOV-2024.php",
    ],
    "3_1": [
        "https://www.nriitexamcell.com/autonomous/results/3-1-NRIA20-OCT-2022.php",
        "https://www.nriitexamcell.com/autonomous/results/3-1-NRIA20-MAY-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/3-1-NRIA20-OCT-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/3-1-NRIA20-APRIL-2024.php",
        "https://www.nriitexamcell.com/autonomous/results/3-1-NRIA20-OCT-2024.php",
    ],
    "3_2": [
        "https://www.nriitexamcell.com/autonomous/results/3-2-NRIA20-MARCH-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/3-2-NRIA20-OCT-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/3-2-NRIA20-MARCH-2024.php",
        "https://www.nriitexamcell.com/autonomous/results/3-2-NRIA20-OCT-2024.php",
    ],
    "4_1": [
        "https://www.nriitexamcell.com/autonomous/results/4-1-NRIA20-SEPT-2023.php",
        "https://www.nriitexamcell.com/autonomous/results/4-1-NRIA20-FEB-2024.php",
        "https://www.nriitexamcell.com/autonomous/results/4-1-NRIA20-OCT-2024.php",
    ],
    "4_2": [
        "https://www.nriitexamcell.com/autonomous/results/4-2-NRIA20-APRIL-2024.php"
    ],
}

def get_student_info_and_results(url, roll_number):
    payload = {"roll": roll_number, "submit": "Get result"}
    session = requests.Session()
    try:
        response = session.post(url, data=payload, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Get student information
        student_info = {}
        
        # Find the name
        name_td = soup.find('td', string='Name of the Student:')
        if name_td and name_td.find_next_sibling('td'):
            student_info['name'] = name_td.find_next_sibling('td').text.strip()
        
        # Get subject results
        tables = soup.find_all("table", class_="dtlsbdr")
        if not tables:
            return {}, student_info

        headers = [th.text for th in tables[-1].find_all("th")]
        try:
            status_index = headers.index("Status")
            subject_index = headers.index("Subject Name")

            rows = tables[-1].find_all("tr")[0:]
            subjects_status = {}

            for row in rows:
                cols = row.find_all("td")
                if len(cols) > max(subject_index, status_index):
                    subject = cols[subject_index].text.strip()
                    status = cols[status_index].text.strip()
                    subjects_status[subject] = status
                    
            return subjects_status, student_info
        except (ValueError, IndexError):
            return {}, student_info
            
    except Exception as e:
        print(f"Error fetching from {url}: {e}")
        return {}, {}

def process_semester(semester, links, roll_number):
    sem_result = {}
    student_info = {}
    
    for url in links:
        subjects, info = get_student_info_and_results(url, roll_number)
        sem_result.update(subjects)  # overwrite with latest attempts
        if info:
            student_info.update(info)
            
    return semester, sem_result, student_info

def compile_full_result(roll_number):
    final_result = {}
    student_info = {}
    has_any_results = False
    failed_subjects_count = 0
    
    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        
        for semester, links in results_links.items():
            future = executor.submit(process_semester, semester, links, roll_number)
            futures.append(future)
        
        for future in futures:
            semester, sem_result, info = future.result()
            final_result[semester] = sem_result
            
            # Count failed subjects
            for subject, status in sem_result.items():
                if status.lower() == 'fail':
                    failed_subjects_count += 1
                    
            if sem_result:  # Check if any subjects were found
                has_any_results = True
            if info:
                student_info.update(info)
                
    return final_result, student_info, has_any_results, failed_subjects_count

@app.context_processor
def utility_processor():
    def now():
        return datetime.now()
    return dict(now=now)
  
@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    student_info = {}
    roll_number = ""
    has_any_results = False
    failed_subjects_count = 0
    
    if request.method == 'POST':
        roll_number = request.form.get('roll_number')
        if roll_number:
            result, student_info, has_any_results, failed_subjects_count = compile_full_result(roll_number)
            
    semester_names = {
        "1_1": "1st Year - 1st Semester",
        "1_2": "1st Year - 2nd Semester",
        "2_1": "2nd Year - 1st Semester",
        "2_2": "2nd Year - 2nd Semester",
        "3_1": "3rd Year - 1st Semester",
        "3_2": "3rd Year - 2nd Semester",
        "4_1": "4th Year - 1st Semester",
        "4_2": "4th Year - 2nd Semester"
    }
            
    return render_template('index.html',
                           result=result,
                           student_info=student_info,
                           roll_number=roll_number,
                           semester_names=semester_names,
                           has_any_results=has_any_results,
                           failed_subjects_count=failed_subjects_count)

if __name__ == '__main__':
    app.run(debug=True)