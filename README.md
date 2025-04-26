# NRIIT Results Portal

A Flask web application that provides a consolidated view of academic results for students of NRIIT.


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ejjadaakhil-13/NRIIT_EXAM-RESULT_SCRAPPER.git
   
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   
   ```

3. Install the required packages:
   ```
   pip install flask requests beautifulsoup4
   
   ```

## Project Structure

```
nriit_results_app/
├── app.py
└── templates/
    └── index.html
```

- `app.py`: Main application file with Flask routes and result processing logic
- `templates/index.html`: HTML template with Bootstrap styling for the user interface

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to http://127.0.0.1:5000/

3. Enter your roll number (format: 20KN1A0XXX) and click Search

 ![image](https://github.com/user-attachments/assets/96559566-b5ed-457e-9988-618da6582218)

4. View your consolidated academic results across all semesters
   
![ScreenRecording2025-04-24190254-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/45899594-74fd-4867-8a6d-b7a446a4f37b)

   
## Current Limitations

- Currently only supports the 2020-2024 batch of students
- Can only show exam results up to April 2025
- Future exam cycles will require updates to the URL database
- Cannot display updated results for subjects passed through revaluation
- Only shows the most recent attempt result for each subject

## How It Works

1. The application maintains a database of result URLs for each semester and examination cycle
2. When a roll number is submitted, the app fetches results from all applicable URLs
3. Results are processed in parallel using Python's ThreadPoolExecutor
4. The compiled results are displayed in a clean, responsive interface with status indicators

## Requirements

- Python 3.6+
- Flask
- Requests
- BeautifulSoup4
- Internet connection to fetch results from the NRIIT server

## Note
This is version 1.0 of the application. An improved version 2.0 with additional features like displaying remaining supplies, CGPA/SGPA calculations, and support for multiple regulations and batches is available at: https://github.com/ejjadaakhil-13/B.TECH_RESULT_SCRAPPER_2.0
