# flask-gemini-demo

This is a python Flask app demonstrating basic Gemini usage. 

The app allows users to upload documents and Gemini will provide a summary of the document content.

## How to run
1. Get a API from [Google AI Studio](https://aistudio.google.com/)

2. Clone this repo.

3. Set up python virtual env; ensure the commands are executed within the environment.

```
cd [proj_dir]
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Copy the `env` file and add the Gemini API.

```
cp .env.sample .env
GEMINI_API_KEY=<api_key>
```

5. Run the app within the virtual environment.
```
python app.py
```

Browse the app at http://127.0.0.1:9999.

Upload a `doc` file or `pdf` file and wait for the result.