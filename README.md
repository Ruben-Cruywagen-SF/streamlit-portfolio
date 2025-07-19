# Sales Report Generator

A professional, interactive Streamlit app that allows users to upload or generate dummy sales data, explore insights visually, export Excel reports, and generate AI-powered summaries — all in one place.

---

## Features

- Dummy data auto-generated on app load
- Download dummy data CSV file
    - Add your own custom data (keeping columns as is)
    - Upload to replace dummy data
- Filter by Region, Rep, and Date  
- View dynamic, interactive charts:  
    - Sales by Region  
    - Sales by Rep (Pie Chart)  
    - Cumulative Sales Over Time  
    - Top Products  
- Generate a downloadable Excel report (pre-formatted summary + data)  
- Get an AI-generated insight paragraph based on the filtered data (powered by Gemini API)  
- Custom theming and styling

---

## Demo

You can try a live version here:  
[streamlit.app link](https://your-app.streamlit.app)

---

## Sample Data Format

| Date       | Region | Rep     | Product   | Sales   |
|------------|--------|---------|-----------|---------|
| 2024-05-01 | North  | Alice   | Widget A  | 580.25  |

Use the **Download Dummy Sales Data** button to get an example CSV file.

---

## Local Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/sales-report-generator.git
cd sales-report-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. (Optional) Get your own Gemini API key and set it as an enviroment vaiable:  
macOS/Linux
```bash
export GEMINI_KEY=yourkeyhere
```
  Windows PowerShell:
```powershell
$env:GEMINI_KEY="yourkeyhere"
```
