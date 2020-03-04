from flask import Flask, render_template, request, jsonify

from datetime import datetime

app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/taskbullet2')
def taskbullet2():
    return render_template('taskbullet(2).html')

@app.route('/taskbullet3')
def taskbullet3():
    return render_template('taskbullet(3).html')

@app.route('/accounts1')
def accounts1():
    return render_template('accounts(1).html')

@app.route('/accounts2')
def accounts2():
    return render_template('accounts(2).html')


@app.route('/save', methods=['POST'])
def save():
    partname_receive = request.form['partname_give']
    name_receive = request.form['name_give']
    date_receive = request.form['date_give']
    taskdetails_receive = request.form['taskdetails_give']
    taskcontents1_receive = request.form['taskcontents1_give']
    taskcontents2_receive = request.form['taskcontents2_give']
    taskcontents3_receive = request.form['taskcontents3_give']
    task_note1_receive = request.form['task_note1_give']
    task_note2_receive = request.form['task_note2_give']
    task_note3_receive = request.form['task_note3_give']

    num = int(db.save_data.count())  # 현재 컬렉션 도큐먼트가 몇개 있는지 알아오기

    print(partname_receive, name_receive, date_receive,
          taskdetails_receive, taskcontents1_receive, taskcontents2_receive, taskcontents3_receive,
          task_note1_receive, task_note2_receive, task_note3_receive)

    doc = {
        'number': num + 1,
        'part_name': partname_receive,
        'name': name_receive,
        'date': date_receive,
        'task_details': taskdetails_receive,
        'task_contents1': taskcontents1_receive,
        'task_contents2': taskcontents2_receive,
        'task_contents3': taskcontents3_receive,
        'note1': task_note1_receive,
        'note2': task_note2_receive,
        'note3': task_note3_receive,
    }

    db.save_data.insert_one(doc)

    return jsonify({'result': 'success'})

@app.route('/save', methods=['GET'])
def look():
    saves = list(db.save_data.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'saves': saves})


@app.route('/detail', methods=['GET'])
def detail():
    num = request.args.get('id')
    print(num)

    result = list(db.save_data.find({'number': int(num)}, {'_id':0}))[0]

    print(result)

    return render_template('taskbullet(4).html', part_name=result['part_name'], name=result['name'],
                           date=result['date'], task_details=result['task_details'],
                           task_contents1=result['task_contents1'], task_contents2=result['task_contents2'],
                           task_contents3=result['task_contents3'], task_note1=result['note1'], task_note2=result['note2'],
                           task_note3=result['note3'])


@app.route('/remove', methods=['POST'])
def remove():
    num = request.form['id']
    print(num)

    db.save_data.delete_one({'number': int(num)})

    return jsonify({'result': 'success'})


@app.route('/save_accounts', methods=['POST'])
def save_accounts():
    name1_receive = request.form['name1_give']
    phone_receive = request.form['phone_give']
    fax_receive = request.form['fax_give']
    email_receive = request.form['email_give']
    note_receive = request.form['note_give']


    num = int(db.save_accounts.count())  # 현재 컬렉션 도큐먼트가 몇개 있는지 알아오기

    print(name1_receive, phone_receive,
          fax_receive, email_receive, note_receive)

    doc = {
        'number': num + 1,
        'name1': name1_receive,
        'phone': phone_receive,
        'fax': fax_receive,
        'email': email_receive,
        'note': note_receive,
        }
    db.save_accounts.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/save_accounts', methods=['GET'])
def accounts_look():
    accounts = list(db.save_accounts.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'accounts': accounts})

@app.route('/details', methods=['GET'])
def details():
    num = request.args.get('id')
    print(num)

    results = list(db.save_accounts.find({'number': int(num)}, {'_id':0}))[0]

    print(results)

    return render_template('accounts(3).html', name1=results['name1'],
                           phone=results['phone'], fax=results['fax'],
                           email=results['email'], note=results['note'])

@app.route('/remove_accounts', methods=['POST'])
def remove_accounts():
    num = request.form['id']
    print(num)

    db.save_accounts.delete_one({'number': int(num)})

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)








