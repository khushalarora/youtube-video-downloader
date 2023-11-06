from flask import Flask, request, render_template, send_file
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
import os

app = Flask(__name__)

print(app.root_path)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        link = request.form.get('Link')
        val = Download(link)
        success = val[0]
        path = val[1]
        if success:
            message = 'Download is completed successfully'
            return render_template('download.html', message=message, file_path=path)
        else:
            # return f"An error has occurred: {message}", 500, path
            message = 'Download unsuccessfull'
            return render_template('download.html', message=message, file_path=path)


@app.route('/<path:filename>', methods=['GET'])
def download(filename):
    filename = os.path.join('/', filename)
    return send_file(filename, as_attachment=True)

def Download(link):
    path = None
    try:
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.filter(res="360p", progressive="true")[0]
        path = youtubeObject.download()
        return True, path
    except Exception as e:
        return False, path


@app.errorhandler(FileNotFoundError)
def handle_file_not_found_error(e):
    return "File not found", 404  # Return a 404 Not Found response

@app.errorhandler(AgeRestrictedError)
def handle_age_restricted_error(error):
    return "Video is Age Restricted", 403


if __name__ == '__main__':
    app.run()


# https://www.youtube.com/watch?v=4gNaG4g6xdM

# heroku local web