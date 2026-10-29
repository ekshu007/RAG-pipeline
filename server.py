from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain.tools import tool
from memory import get_chat_history
from fastapi import UploadFile,File
from interview_tools import search_jobs
from interview_prep.parser import extract_resume_text
from interview_prep.gap_analysis import analyze_skill_gap
from interview_prep.interviewer import generate_questions
from interview_prep.gap_analysis import analyze_skill_gap
import json
from fastapi import UploadFile, File,Form
from interview_prep.skill_extractor import extract_skills
from interview_prep.recruitement_tools import extract_job_skills
from services.announcement_service import get_latest_announcement

from agent import employee_agent, hr_agent
from db import get_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Request Models
# ----------------------------

class ChatRequest(BaseModel):
    message: str
    employee_id: int
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str

from services.announcement_service import generate_announcement, save_announcement

class AnnouncementRequest(BaseModel):
    topic:str
    created_by:str

@app.post("/generate-announcement")
def create_announcement(data:AnnouncementRequest):

    announcement = generate_announcement(data.topic)

    save_announcement(
        announcement["title"],
        announcement["content"],
        data.created_by
    )

    return announcement
# ----------------------------
# Home
# ----------------------------

@app.get("/")
def home():
    return {
        "message": "HR Assistant API is running"
    }


# ----------------------------
# Login
# ----------------------------

@app.post("/login")
def login(request: LoginRequest):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            username,
            employee_id,
            role
        FROM users
        WHERE username=%s
        AND password=%s
        """,
        (request.username, request.password)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        return {
            "success": False,
            "message": "Invalid username or password"
        }

    return {
        "success": True,
        "username": user["username"],
        "employee_id": user["employee_id"],
        "role": user["role"]
    }
@app.post("/interview-readiness/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    role: str = Form(...)
):

    # 1. Save resume
    contents = await file.read()


    # 2. Extract resume text
    resume_text = extract_resume_text(contents)


    # 3. Extract skills
    candidate_skills = extract_skills(resume_text)


    # 4. Get job skills
    required_skills = extract_job_skills(role)


    # 5. Match percentage
    match_percentage = analyze_skill_gap(
        candidate_skills,
        required_skills
    )


    result = {
        "candidate_skills": candidate_skills,
        "required_skills": required_skills,
        "match_percentage": match_percentage
    }


    # 6. Interview questions
    if match_percentage >= 80:

        questions = generate_questions(
            candidate_skills
        )

        result["status"] = "Interview recommended"
        result["questions"] = questions

    else:

        result["status"] = "Skill gap detected"
        result["questions"] = []


    return result


@app.get("/announcement")
def announements():
    return get_latest_announcement()
# ----------------------------
# Normal Chat
# ----------------------------
from memory import get_chat_history


@app.post("/chat")
def chat(request: ChatRequest):

    user_context = f"""
Logged in employee id: {request.employee_id}
User role: {request.role}
"""

    if request.role.lower() == "hr":
        agent = hr_agent
    else:
        agent = employee_agent

    # Create session id
    session_id = f"{request.role}_{request.employee_id}"

    # Get chat history
    history = get_chat_history(session_id)
    #Add login Context only once
    if len(history.messages)==0:
        history.add_user_message(user_context)
    history.add_user_message(request.message)

    # Invoke agent with full conversation history
    response = agent.invoke(
        {
            "messages": history.messages
        }
    )

    # Extract AI response
    ai_response = response["messages"][-1].content

    # Save AI response to memory
    history.add_ai_message(ai_response)

    return {
        "response": ai_response
    }
@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        employee_id,
        name,
        department,
        role,
        joining_date FROM employees
        WHERE employee_id = %s
    """

    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    if employee is None:
        return {
            "success": False,
            "message": "Employee not found"
        }

    employee["joining_date"] = str(employee["joining_date"])

    return {
        "success": True,
        "employee": employee
    }
# ----------------------------
# Streaming Chat
# ----------------------------
@app.post("/chat-stream")
async def chat_stream(request: ChatRequest):

    user_context = f"""
Logged in employee id: {request.employee_id}
User role: {request.role}
"""

    if request.role.lower() == "hr":
        agent = hr_agent
    else:
        agent = employee_agent

    # Session memory
    session_id = f"{request.role}_{request.employee_id}"
    history = get_chat_history(session_id)

    # Add login context only once
    if len(history.messages) == 0:
        history.add_user_message(user_context)

    # Add current user message
    history.add_user_message(request.message)

    ai_response = ""

    async def generate():

        nonlocal ai_response

        async for event in agent.astream_events(
            {
                "messages": history.messages
            },
            version="v2"
        ):

            event_type = event.get("event")

            # ------------------------
            # Tool Started
            # ------------------------
            if event_type == "on_tool_start":

                tool_name = event.get("name", "Tool")

                yield (
                    f"data: {json.dumps({'type':'status','content':f'🔍 Using {tool_name}...'})}\n\n"
                )

            # ------------------------
            # Tool Finished
            # ------------------------
            elif event_type == "on_tool_end":

                tool_name = event.get("name", "Tool")

                yield (
                    f"data: {json.dumps({'type':'status','content':f'✅ Finished {tool_name}'})}\n\n"
                )

            # ------------------------
            # Model Streaming
            # ------------------------
            elif event_type == "on_chat_model_stream":

                chunk = event["data"]["chunk"]

                if hasattr(chunk, "content") and chunk.content:

                    ai_response += chunk.content

                    yield (
                        f"data: {json.dumps({'type':'token','content':chunk.content})}\n\n"
                    )

        # Save assistant reply in memory
        history.add_ai_message(ai_response)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )