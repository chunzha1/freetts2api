# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

conda activate say_env
req: pip install flask
gunicorn
flask_cors

cd /Volumes/WD_sn770/say_command
python app.py
python test.py or

curl -X POST -d "text=Hello, world" -d "voice=Cello" http://localhost:8083/tts > test.m4a


new oaiapi tts-1
curl -X POST -H "Authorization: Bearer y1our_api_key_here" -H "Content-Type: application/json" -d '{"input": "The quick brown fox jumped over the lazy dog.", "voice": "Samantha", "model": "tts-1"}' http://localhost:8083/v1/audio/speech --output speech.mp3


pip freeze > requirements.txt
