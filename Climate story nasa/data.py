from flask import Flask, request, jsonify
from flask_cors import CORS
import openpyxl
import os

app = Flask(__name__)
CORS(app)
# Load or create the Excel file
def load_or_create_excel():
    # Check if the Excel file exists, and load or create it
    if os.path.exists("contact_data.xlsx"):
        workbook = openpyxl.load_workbook("contact_data.xlsx")
        sheet = workbook.active
    else:
        # Create a new workbook and add headers if it doesn't exist
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Name", "Email", "Message"])
        workbook.save("contact_data.xlsx")  # Save the new workbook
    return workbook, sheet

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()  # Get the JSON data from the request
        
        # Check if data is None or empty
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Validate the data
        if not name or not email or not message:
            return jsonify({"status": "error", "message": "All fields are required"}), 400

        # Load or create the Excel file and sheet
        workbook, sheet = load_or_create_excel()

        # Append the form data to the Excel sheet
        sheet.append([name, email, message])

        # Save the Excel file
        workbook.save("contact_data.xlsx")

        return jsonify({"status": "success", "message": "Form data saved to Excel"}), 200

    except Exception as e:
        print(f"Error: {e}")  # Print the error to console for debugging
        return jsonify({"status": "error", "message": str(e)}), 500  # Return an error message

if __name__ == "__main__":
    app.run(debug=True,port=5500)
