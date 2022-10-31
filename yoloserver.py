from flask import Flask, send_from_directory, request, jsonify, Response
import pymysql
import os
import time
import threading

sema = threading.Semaphore(1)

ht='localhost'
pt=3306
pw=''

def db_connect():
    return pymysql.connect(host=ht, port=pt, user='root', passwd=pw, db='congestion_db', charset='utf8')

app = Flask(__name__, static_url_path='/', static_folder='build')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file and allowed_file(file.filename.lower()):
            sta = time.time() # 시간 측정
            sema.acquire() # 세마포어 획득

            # 파일을 a.jpg/a.png/a.jpeg 형식으로 저장
            filename = 'a.' + file.filename.rsplit('.', 1)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # 이미지로 부터 사람 수 예측
            res = pplcounter.count_people(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sema.release() # 세마포어 릴리즈
            return jsonify([str(res), f'{time.time() - sta:.2f}'])
    except Exception as e:
        print(e)
    # unsupported media type (=http status 415)
    return Response('Error', status=415, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port='4500')