# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from flask import Flask, flash, render_template, request, redirect, send_from_directory
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

__author__ = 'Elliot Thornton - The Language Conservancy'

model_name = "facebook/wav2vec2-xlsr-53-espeak-cv-ft"
## model_name = "facebook/wav2vec2-lv-60-espeak-cv-ft"

tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("asr.html", model=model_name)

@app.route('/wav/<path:filename>')
def download(filename):
    path = os.path.join(APP_ROOT, 'wav/')
    return send_from_directory(
        path,
        filename,
        as_attachment=True,
        mimetype='audio/wav'
    )
@app.route('/js/<path:filename>')
def downloadjs(filename):
    path = os.path.join(APP_ROOT, 'js/')
    return send_from_directory(
        path,
        filename,
        as_attachment=True,
        mimetype='text/javascript'
    )

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'wav/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        audio, rate = librosa.load(destination, sr = 16000)
        input_values = tokenizer(audio, return_tensors = "pt").input_values
        logits = model(input_values).logits
        prediction = torch.argmax(logits, dim = -1)
        transcription = tokenizer.batch_decode(prediction)[0]
        print(transcription)
        
        return render_template("asr.html", model=model_name, file=filename, transcription=transcription, prediction=prediction[0], logits=logits)

    
import os
import uuid
from flask import Flask, flash, request, redirect




@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    filename = str(uuid.uuid4()) + ".wav"
    destination = os.path.join(APP_ROOT, 'wav/', filename)
    file.save(destination)
    audio, rate = librosa.load(destination, sr = 16000)
    input_values = tokenizer(audio, return_tensors = "pt").input_values
    logits = model(input_values).logits
    prediction = torch.argmax(logits, dim = -1)
    transcription = tokenizer.batch_decode(prediction)[0]
    print(transcription)
    print(logits[0])
    return render_template("asr.html", model=model_name, file=filename, transcription=transcription, prediction=prediction[0], logits=logits)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4555, debug=True)