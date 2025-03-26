from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware

OPENAI_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDIyOTFAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.DuTpd4IaEMZT5E5c2ZZgt7s2bhrpn5VOurdBiwZLK4s'

app = FastAPI()

# Allow CORS for all origins (you can customize as needed)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow these methods
    allow_headers=["*"],
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_ticket_status",
            "description": "Checks and returns the status of a ticket using the specified ticket_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "integer",
                        "description": "The value of ticket id whose status needs to be checked"
                    }
                },
                "required": ["ticket_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_meeting",
            "description": "Schedules a meeting on a specified date at specified time in a specified meeting_room",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date of the meeting to schedule"
                    },
                    "time": {
                        "type": "string",
                        "description": "The time of the meeting to schedule"
                    },
                    "meeting_room": {
                        "type": "string",
                        "description": "The room name of the meeting to schedule. eg: 'Room A'"
                    }
                },
                "required": ["date","time","meeting_room"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_expense_balance",
            "description": "Retreves the current expense balance of a specified employee id",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer",
                        "description": "The id of the employee whose expense balance needs to be retrieved."
                    },
                },
                "required": ["employee_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_performance_bonus",
            "description": "Calculates the performance bonus of a specified employee for a specified year.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer",
                        "description": "The id of the employee whose performance bonus needs to be calculated."
                    },
                    "current_year": {
                        "type": "integer",
                        "description": "The year for which the performance bonus needs to be calculated."
                    },
                    
                },
                "required": ["employee_id","current_year"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "report_office_issue",
            "description": "Reports an office issue by specifying the department and issue code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_code": {
                        "type": "integer",
                        "description": "The code of the issue that is being reported"
                    },
                    "department": {
                        "type": "integer",
                        "description": "The department name related to which the issue is being reported."
                    },
                    
                },
                "required": ["issue_code","department"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
]

async def query_gpt(user_input: str):
    url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": user_input}],
        "tools": tools,
        "tool_choice": "auto",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            print(response)
            # Check if the response is successful
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise HTTPException(status_code=400, detail="Error from OpenAI API")

    except Exception as e:
        # General exception handling for unexpected errors
        raise HTTPException(status_code=500, detail=f"Task processing failed: {str(e)}")


@app.get("/execute")
async def qet_response(q:str):
    response = await query_gpt(user_input=q)
    response = response["choices"][0]["message"]["tool_calls"][0]["function"]
    func_name = response["name"]
    func_args = response["arguments"]
    return {"name": func_name, "arguments":func_args}