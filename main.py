# --------------------------- #
# Made by GorouFlex           #
# Ported from rfoal/duolingo  #
# Version 1.7                 #
# --------------------------- #
import os
import requests
import json
import base64
import time
import shutil
from configparser import ConfigParser
from getpass import getpass
from datetime import datetime

# Define ANSI escape code, i don't want to use colorama since i cannot figure how to make it works on cross-platform
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'

# Define where and the name for Config folder and some assset
config_folder: str = 'Config'
config_path: str = f'{config_folder}/DuoXPyConfig.txt'

config: ConfigParser = ConfigParser()
config.read(config_path)

# Print information window
print(f"{colors.WARNING}------- Welcome to DuoXPy -------{colors.ENDC}")
print(f"{colors.OKBLUE}Made by GFx{colors.ENDC}")
# If this script were on GitHub Actions
if os.getenv('GITHUB_ACTIONS') == 'true':
    print(f"{colors.OKBLUE}Powered by GitHub Actions V3 and Python{colors.ENDC}")
    print(f"{colors.OKGREEN}Run with GitHub Actions: Yes{colors.ENDC}")
    print(f"{colors.WHITE}Current repo: {os.getenv('GITHUB_REPOSITORY')}{colors.ENDC}")
    # Check repo commit 
    user_repo = os.getenv('GITHUB_REPOSITORY')
    ORIGINAL_REPO = 'Kdragonxx/DuoXPy'
    user_url = f'https://api.github.com/repos/{user_repo}/commits?path=main.py'
    original_url = f'https://api.github.com/repos/{ORIGINAL_REPO}/commits?path=main.py'
    user_response = requests.get(user_url, timeout=10000)
    original_response = requests.get(original_url, timeout=10000)
    # If the API response 200 not other code to prevent some unexpected things
    if user_response.status_code == 200 and original_response.status_code == 200:
        user_commit = user_response.json()[0]['sha']
        original_commit = original_response.json()[0]['sha']
        if user_commit == original_commit:
            print(f"{colors.OKGREEN}Your repo is up-to-date with the original repo{colors.ENDC}")
        else:
            print(f"{colors.WARNING}Your repo is not up-to-date with the original repo{colors.ENDC}")
            print(f"{colors.FAIL}Please update your repo to the latest commit{colors.ENDC}{colors.FAIL} to get new updates and bug fixes{colors.ENDC}")
    else:
        print(f"{colors.WARNING}--------- Traceback log ---------{colors.ENDC}\n{colors.FAIL}❌ Error code 4: Failed to fetch commit information\nPlease refer to: https://github.com/gorouflex/HoneygainPot/blob/main/Docs/Debug.md for more information\nOr create an Issue on GitHub if it still doesn't work for you.{colors.ENDC}")
    print(f"{colors.WARNING}Lessons: {os.getenv('LESSONS')}{colors.ENDC}")
else:
    print(f"{colors.FAIL}Run with GitHub Actions: No{colors.ENDC}")
    try:
        lessons = config.get('User', 'LESSONS')
        print(f"{colors.WARNING}Lessons: {lessons}{colors.ENDC}")
    except:
        print(f"{colors.WARNING}Lessons: N/A{colors.ENDC}")
print(f"{colors.WHITE}Codename: Sandy{colors.ENDC}")
print(f"{colors.WHITE}Config folder:", os.path.join(os.getcwd(), f"{colors.WHITE}Config{colors.ENDC}"))
print(f"{colors.WARNING}---------------------------------{colors.ENDC}")
print(f"{colors.WHITE}Starting DuoXPy{colors.ENDC}")
print(f"{colors.WHITE}Collecting information...{colors.ENDC}")

# Take token information and save it to config
def create_config() -> None:
    config.add_section('User')
    config.set('User', 'TOKEN', "")
    if os.getenv('GITHUB_ACTIONS') == 'true':
        token = os.getenv('JWT_TOKEN')
        config.set('User', 'TOKEN', f"{token}")
        lessons = os.getenv('LESSONS')
        lessonType = os.getenv('LESSON_TYPE')
    else:
        token = getpass(f"{colors.WHITE}Token: {colors.ENDC}")
        config.set('User', 'TOKEN', f"{token}")
        lessons = getpass(f"{colors.WHITE}Lesson: {colors.ENDC}")
        lessonType = getpass(f"{colors.WHITE}Lesson Type (Skill/Practice): {colors.ENDC}")
    print("env")
    print(os.environ)
    config.set('User', 'LESSONS', f"{lessons}")
    config.set('User', 'LESSON_TYPE', f"{lessonType}")
    with open(config_path, 'w', encoding='utf-8') as configfile:
        configfile.truncate(0)
        configfile.seek(0)
        config.write(configfile)

# Check if Config it's exist or not?
def check_config_integrity() -> None:
    if not os.path.exists(config_folder):
        print(f"{colors.WARNING}Creating new config folder at:", os.path.join(os.getcwd()))
        os.mkdir(config_folder)
    
    if not os.path.isfile(config_path) or os.stat(config_path).st_size == 0:
        create_config()
        return
    
    config.read(config_path)
    
    if not config.has_section('User') or not config.has_option('User', 'TOKEN') or not config.has_option('User', 'LESSONS'):
        create_config()

check_config_integrity()
config.read(config_path)

# Take token from config

try:
    token = config.get('User', 'TOKEN')
    lessons = config.get('User', 'LESSONS')
    lessonType = config.get('User', 'LESSON_TYPE')
    print("Lesson-Type", config.get('User', 'LESSON_TYPE'))
except:
    create_config()

# Configure headers for futher request
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

# Token processing 
try:
    jwt_token = token.split('.')[1]
except:
    print(f"{colors.WARNING}--------- Traceback log ---------{colors.ENDC}\n{colors.FAIL}❌ Invalid token{colors.ENDC}")
    exit(-1)

padding = '=' * (4 - len(jwt_token) % 4)
sub = json.loads(base64.b64decode(jwt_token + padding).decode())

# Collect date and insert to the API
# date = datetime.now().strftime('%Y-%m-%d')
date = "2017-06-30"
print(f"{colors.WARNING}Date: {date}{colors.ENDC}")
response = requests.get(
    f"https://www.duolingo.com/{date}/users/{sub['sub']}?fields=fromLanguage,learningLanguage,xpGains",
    headers=headers,
)
data = response.json()
# Take element required to make a request
fromLanguage = data['fromLanguage']
learningLanguage = data['learningLanguage']
try:
    xpGains = data['xpGains']
    skillId = xpGains[0]['skillId']
except:
    print(f"{colors.FAIL}Your Duolingo account has been banned or does not exist{colors.ENDC}")
    exit(-1)

skillId = next(
    (xpGain['skillId'] for xpGain in reversed(xpGains) if 'skillId' in xpGain),
    None,
)
print(f"From (Language): {fromLanguage}")
print(f"Learning (Language): {learningLanguage}")

print(date)

# Do a loop and start make request to gain xp
for i in range(int(lessons)):
    session_data = {
        'challengeTypes': [
            'assist',
            'characterIntro',
            'characterMatch',
            'characterPuzzle',
            'characterSelect',
            'characterTrace',
            'completeReverseTranslation',
            'definition',
            'dialogue',
            'form',
            'freeResponse',
            'gapFill',
            'judge',
            'listen',
            'listenComplete',
            'listenMatch',
            'match',
            'name',
            'listenComprehension',
            'listenIsolation',
            'listenTap',
            'partialListen',
            'partialReverseTranslate',
            'readComprehension',
            'select',
            'selectPronunciation',
            'selectTranscription',
            'syllableTap',
            'syllableListenTap',
            'speak',
            'tapCloze',
            'tapClozeTable',
            'tapComplete',
            'tapCompleteTable',
            'tapDescribe',
            'translate',
            'typeCloze',
            'typeClozeTable',
            'typeCompleteTable',
        ],
        'fromLanguage': fromLanguage,
        'isFinalLevel': False,
        'isV2': True,
        'juicy': True,
        'learningLanguage': learningLanguage,
        'smartTipsVersion': 2,
        'type': 'GLOBAL_PRACTICE'
    }

    session_response = requests.post(f'https://www.duolingo.com/{date}/sessions', json=session_data, headers=headers)
    if session_response.status_code == 500:
         print(f"{colors.FAIL}Session Error 500 / No skillId found in xpGains or Missing some element to make a request\nPlease do at least 1 or some lessons in your skill tree\nVisit https://github.com/gorouflex/DuoXPy#how-to-fix-error-500---no-skillid-found-in-xpgains for more information{colors.ENDC}")
         continue
    elif session_response.status_code != 200:
         print(f"{colors.FAIL}Session Error: {session_response.status_code}, {session_response.text}{colors.ENDC}")
         continue
    session = session_response.json()

    end_response = requests.put(
        f"https://www.duolingo.com/{date}/sessions/{session['id']}",
        headers=headers,
        json={
            **session,
            'heartsLeft': 0,
            'startTime': (time.time() - 60),
            'enableBonusPoints': False,
            'endTime': time.time(),
            'failed': False,
            'maxInLessonStreak': 9,
            'shouldLearnThings': True,
        },
    )

    try:
        end_data = end_response.json()
    except json.decoder.JSONDecodeError as e:
        print(f"{colors.FAIL}Error decoding JSON: {e}{colors.ENDC}")
        print(f"Response content: {end_response.text}")
        continue

    response = requests.put(f'https://www.duolingo.com/{date}/sessions/{session["id"]}', data=json.dumps(end_data), headers=headers)
    if response.status_code == 500:
         print(f"{colors.FAIL}Response Error 500 / No skillId found in xpGains or Missing some element to make a request\nPlease do at least 1 or some lessons in your skill tree\nVisit https://github.com/gorouflex/DuoXPy#how-to-fix-error-500---no-skillid-found-in-xpgains for more information{colors.ENDC}")
         continue
    elif response.status_code != 200:
         print(f"{colors.FAIL}Response Error: {response.status_code}, {response.text}{colors.ENDC}")
         continue
    print(f"{colors.OKGREEN}[{i+1}] - {end_data['xpGain']} XP{colors.ENDC}")

# Delete Config folder after running done on GitHub Actions (idk if it's useful or not)
if os.getenv('GITHUB_ACTIONS') == 'true':
    try:
      shutil.rmtree(config_folder)
      print(f"{colors.WARNING}Cleaning up..{colors.ENDC}")
    except Exception as e:
      print(f"{colors.FAIL}Error deleting config folder: {e}{colors.ENDC}")
      exit(-1)

print("Closing DuoXPy ✅")
