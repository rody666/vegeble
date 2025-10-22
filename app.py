from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from openai import OpenAI
import os
import base64
from api_key import apikey

app = Flask(__name__)
client = OpenAI(api_key=apikey.key)

prompt = """
You are a vegetable assessment AI. Follow these rules strictly:

1. Input: the name of the vegetable and a short description of its condition.
2. Output must be in valid JSON format only, in one line.
3. JSON must contain the following three keys:
   - "vegetable": the name of the vegetable (in Japanese)
   - "condition": a number between 0.0 and 1.0 
       (0 = unsellable, 1 = perfect, like supermarket quality)
   - "reason": 
       - If the condition is 0.7 or lower, describe the reason in Japanese (e.g., "傷がある", "色が悪い").
       - If the condition is higher than 0.7, output "none".
4. Keep the output concise and consistent with the examples.
5. Examples:
   Input: "Tomato, slightly wilted"
   Output: {"vegetable": "トマト", "condition": 0.7, "reason": "少ししなびている"}
   Input: "Cabbage, firm leaves, no damage"
   Output: {"vegetable": "キャベツ", "condition": 1.0, "reason": "none"}

Input: "{vegetable_description}"
"""


def price(image_type,image_base64):
    image_data_url = f"data:image/{image_type};base64,{image_base64}"
    try: 
        response = client.responses.create(
            model="gpt-5",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        },
                        {
                            "type": "input_image",
                            "image_url": image_data_url
                        }
                    ]
                }
            ]
        )
        return response.output_text
    except Exception as e:
        # Capture full traceback so the runtime error can be inspected
        import traceback
        tb = traceback.format_exc()
        # Print to console (Flask dev server stdout) and return so the template can show it
        print("Error in price():", tb)
        return f"ERROR in price(): {e}\n{tb}"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'heif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('assenssment.html')


@app.route('/assenssment', methods=['POST'])
def assenssment():
    #if 'file' not in request.files:
    #    return 'No file part'
    
    file = request.files['vege_image']
    
    if file.filename == '':
        return 'No selected file'
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )
        file.save(filepath)
        with open(filepath, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        output = price(filename.rsplit('.', 1)[1], encoded)
        return render_template('assenssment.html',encoded=encoded,output=output)
    
    return 'Invalid file type'


if __name__ == '__main__':
    app.run(debug=True)