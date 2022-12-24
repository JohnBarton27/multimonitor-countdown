from flask import Flask, render_template
from datetime import datetime
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

target_time = datetime(year=2022, month=11, day=20, hour=10, minute=00)


@app.route('/')
def hello():
    return render_template('index.html', time_remaining=get_time_remaining())


@socketio.on('time')
def time():
    emit('time_update', get_time_remaining())


def get_time_remaining():
    now = datetime.now()
    time_left = target_time - now

    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours < 10:
        hours = f'0{hours}'

    if minutes < 10:
        minutes = f'0{minutes}'

    if seconds < 10:
        seconds = f'0{seconds}'

    if hours == '00' and minutes == '00':
        return f'{seconds}'

    if hours == '00':
        return f'{minutes}:{seconds}'

    return f'{hours}:{minutes}:{seconds}'

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=1120)
