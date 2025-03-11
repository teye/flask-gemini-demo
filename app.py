import os
import pathlib
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

client = genai.Client(api_key=GEMINI_API_KEY)

def generate(filename, model, additional_prompt):

    # retrieve and encode the doc
    # doc_io = io.BytesIO(httpx.get(doc_link).content)
    file_path = pathlib.Path('./uploads/' + filename)

    sample_doc = client.files.upload(
        file=file_path
    )

    # prepare the video link
    # video = types.Part.from_uri(
    #     file_uri=video_link,
    #     mime_type="video/*"
    # )

    # if additional prompt is not provided, just append a space
    if not additional_prompt:
        additional_prompt = " "
    
    # prepare content to send to the model
    contents = [
        sample_doc,
        types.Part.from_text(text="""Provide a summary of the document."""),
        additional_prompt,
    ]

    # define content configuration
    generate_content_config = types.GenerateContentConfig(
        temperature = 1,
        top_p = 0.95,
        max_output_tokens = 8192,
        response_modalities = ["TEXT"],
    )

    return client.models.generate_content(
        model = model,
        contents = contents,
        config = generate_content_config,
    ).text


# Define the home page route
@app.route('/', methods=['GET'])
def index():
    '''
    Renders the home page.
    Returns:The rendered template.
    '''
    return render_template('index.html')

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    '''
    Summarize the user provided video.
    Returns: Summary
    '''

    # process form data if it is POST
    if request.method == 'POST':
        file = request.files['file']
        doc_link = request.form.get("doc_link", False)
        model = request.form['model']
        additional_prompt = request.form['additional_prompt']

        # generate the summary
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            with open(file_path, 'rb') as f:
                file_bytes = f.read()

            summary = generate(file.filename, model, additional_prompt)
            return summary
            # return None
        
        except ValueError as e:
            raise e
        
    # redirect to home page if request is GET
    else:
        return redirect('/')

# start the server with the 'run()' method
if __name__ == '__main__':
    server_port = os.environ.get('PORT', '9999')
    app.run(debug=True, port=server_port, host='0.0.0.0')