from tinkoff_voicekit_client import ClientSTT
import os
import logging
import soundfile as sf
import psycopg2
from datetime import datetime


logging.basicConfig(level=logging.DEBUG, filename='myapp.log', filemode= 'w',
                        format='%(asctime)s-%(process)d-%(message)s')
def func():
    path = input("Введите где находиться ващ аудиофайл: ")
    number = input("Введите номер телефона: ")
    bd = input("Введите 1, если надо записать в базу данных: ")
    etap = input("Введите этап распознавания 1 или 2: ")
    otvet = 'None'
    time = datetime.today()


    API_KEY = "API_KEY"
    SECRET_KEY = "SECRET_KEY"

    client = ClientSTT(API_KEY, SECRET_KEY)
    f = sf.SoundFile(path)
    audio_config = {
        "encoding": "LINEAR16",
        "sample_rate_hertz": 8000,
        "num_channels": 1
    }
    stream_config = {"config": audio_config}

    # recognise stream method call
    if etap == '1':
        with open(path, "rb") as source:
            responses = client.streaming_recognize(source, stream_config)
            for response in responses:
                s = response[0]['recognition_result']['alternatives'][0]['transcript']
                if s.find('автоответчик') !=-1:
                    otvet = 0
                    logging.warning('АО-{}-{} seconds-{}'.format(number , len(f)/(f.samplerate) ,
                                                            s))
                    result = 'AO'
                else:
                    otvet = 1
                    logging.warning('человек-{}-{} seconds-{}'.format(number, len(f) / (f.samplerate),
                                                            s))
                    result = 'человек'
    elif etap == '2':
        with open(path, "rb") as source:
            responses = client.streaming_recognize(source, stream_config)
            for response in responses:
                s = response[0]['recognition_result']['alternatives'][0]['transcript']
                if s.find('нет') !=-1 or s.find('неудобно') !=-1:
                    otvet = 0
                    logging.warning('отрицательные слова-{}-{} seconds-{}'.format(number, len(f) / (f.samplerate),
                                                                 s))
                    result = 'отрицательные слова'
                elif s.find('говорите') !=-1 or s.find('да конечно'):
                    otvet = 1
                    logging.warning('положительные слова-{}-{} seconds-{}'.format(number, len(f) / (f.samplerate),
                                                                             s))
                    result = 'положительные слова'
    if bd == 1:
        for response in responses:
            s = response[0]['recognition_result']['alternatives'][0]['transcript']
            if s != '':
                break

        conn = psycopg2.connect(dbname='database', user='db_user',
                                password='mypassword', host='localhost')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO таблица (datetime , result, phone, len audio, transcript) values('time', 'result','number', 'len(f) / (f.samplerate)', 's' )')
        conn.close()

    os.remove(path)
    return otvet


if __name__ == "__main__":
    func()
