import os
import google.generativeai as genai
from dotenv import load_dotenv
import typing_extensions as typing
import PIL.Image
from datetime import datetime
from utils import get_active_window_name_windows
import time
import pyautogui
import json
import sqlite3


load_dotenv()

genai.configure(api_key=os.getenv('API_KEY'))

class ActivityDescription(typing.TypedDict):
    goal: str
    is_productive: bool
    activity: str
    explaination: str

class Activity(typing.TypedDict):
    datetime: datetime
    application: str
    activity: str
    goal: str = None
    is_productive: bool = None
    explanation: str = None
    iteration_duration: float = None

DATABASE_FILE = "activity_logs.db"

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEX,
            application TEXT,
            activity TEXT,
            goal TEXT,
            is_productive INTEGER,
            explanation TEXT,
            iteration_duration REAL
        )
    """)
    conn.commit()
    conn.close()

create_table()

def save_activity(activity: Activity):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO activities (datetime, application, activity, goal, is_productive, explanation, iteration_duration)
        VALUES (?, ?, ?, ?, ?, ?, ?)        
        """,
        (
            activity["datetime"].isoformat(),
            activity["application"],
            activity["activity"],
            activity["goal"],
            activity["is_productive"],
            activity["explanation"],
            activity["iteration_duration"],
        ),
    )
    conn.commit()
    conn.close()

model = genai.GenerativeModel("gemini-1.5-flash")

goals = ["coding", "planning trip to kolkata"]
while True:
    img = pyautogui.screenshot()
    print("Screenshot take", time.time())
    iteration_start_time = time.time()

    result = model.generate_content(
        [f"What is going on on this computer screen? Keep it very short and concise. Also you need to classify whether the content is productive ie is helping me achieve my goals - {goals} or not, which goal is it helping in (if any) and a brief and concise explanation why. Coding is always productive, Youtube when used to watch educational or coding related content is productive otherwise isn't . ",
         img],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=list[ActivityDescription]
        ),
    )
    # print(result.text)
    json_response = json.loads(result.text)[0]
    # print(json_response)
    activity = Activity(
        datetime=datetime.now(),
        application=get_active_window_name_windows(),
        activity=json_response.get("activity", None),
        goal=json_response.get("goal", None),
        is_productive=json_response.get("is_productive", None),
        explanation=json_response.get("explanation", None),
    )
    # break
    iteration_end_time = time.time()
    activity["iteration_duration"] = iteration_end_time - iteration_start_time
    save_activity(activity)
    print(activity)
    time.sleep(30)
    
    

