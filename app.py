from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai

# Set your API key for the generative AI
GOOGLE_API_KEY = "AIzaSyC8L1FxK7ksv7vdFIszIshUxQsu_UYkYbA"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

# Initialize Flask app
app = Flask(__name__)

# Route to serve the HTML page
@app.route('/')
def index():
    # This will render the HTML directly from the string in the same file
    return render_template_string(open('index.html').read())

# Route to handle chat interactions
@app.route('/chat', methods=['POST'])
def chat_response():
    try:
        # Retrieve the user's message and language from the incoming JSON
        user_input = request.get_json().get('message')
        target_language = request.get_json().get('language', 'en')  # Default to English if no language provided

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Send the user's message to the generative model
        response_raw = chat.send_message(user_input)
        response = response_raw.text

        return jsonify({"response": response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
