from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"  # Folder to temporarily store uploaded files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_files():
    """Handle the file comparison."""
    file1 = request.files.get('file1')  # Get the first file
    file2 = request.files.get('file2')  # Get the second file

    if not file1 or not file2:
        return "Please upload both files!", 400  # Handle missing files

    # Save the files temporarily
    file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
    file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)
    file1.save(file1_path)
    file2.save(file2_path)

    try:
        # Load Excel files into pandas DataFrames
        df1 = pd.read_excel(file1_path)
        df2 = pd.read_excel(file2_path)
    except Exception as e:
        return f"Error reading Excel files: {e}", 400

    # Compare files: Find rows in df1 that are not in df2 and vice versa
    diff = pd.concat([df1, df2]).drop_duplicates(keep=False)

    # Save the differences to a new Excel file
    output_path = os.path.join(UPLOAD_FOLDER, "differences.xlsx")
    diff.to_excel(output_path, index=False)

    # Send the generated file back to the user
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

