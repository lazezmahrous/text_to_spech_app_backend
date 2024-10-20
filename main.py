from flask import Flask, jsonify , request ,send_from_directory
import os
from gtts import gTTS
import uuid

app = Flask(__name__) 

# Define The Upload Folder
UPLOAD_FOLDER = 'audio_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/text_to_spech', methods=['POST'])
def text_to_spech():
    try:
        #Get Data From Request as JSON
        data = request.get_json()
        text = data['text']
        language = data['language']
        # Convert Text To Speech
        myobj = gTTS(text=text, lang=language, slow=False)
        
        # Generate A Unique File Name For The Audio file
        file_name = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        myobj.save(file_path)
        
        # Return The File URL
        return jsonify({
            "message": "Text to speech conversion successful", 
            "file_url": f"http://192.168.1.9:50374/audio_files/{file_name}"
        })
       
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/audio_files/<filename>', methods=['GET'])
def get_audio(filename):
    
    # Send The File From The Upload Folder
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__': 
    app.run(debug=True , host='0.0.0.0', port=50374)
