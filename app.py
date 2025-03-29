from flask import Flask, request, jsonify, render_template
import difflib

app = Flask(__name__, template_folder='diffCheckFE')

# Helper function to read files
def read_file(file):
    file.seek(0)
    return file.read().decode("utf-8")

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to compare two files and return differences
@app.route('/diff', methods=['POST'])
def diff_files():
    file1 = request.files.get('file1')
    file2 = request.files.get('file2')

    if not file1 or not file2:
        return jsonify({"error": "Both files are required"}), 400
    
    content1 = read_file(file1)
    content2 = read_file(file2)
    
    diff = difflib.unified_diff(content1.splitlines(), content2.splitlines(), lineterm="")
    diff_lines = list(diff)
    
    return jsonify({"diff": diff_lines})

# Route to promote one file's content over the other
@app.route('/promote', methods=['POST'])
def promote_file():
    file1 = request.files.get('file1')
    file2 = request.files.get('file2')
    action = request.form.get('action', 'overwrite')

    if not file1 or not file2:
        return jsonify({"error": "Both files are required"}), 400
    
    content1 = read_file(file1)
    content2 = read_file(file2)

    if action == "overwrite":
        return jsonify({"promoted_content": content1})  # File1's content overwrites file2's content
    elif action == "merge":
        merged_content = content1 + "\n" + content2  # Simple merge
        return jsonify({"promoted_content": merged_content})
    else:
        return jsonify({"error": "Invalid action"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
