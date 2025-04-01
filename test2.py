import json
import os
from fastapi import FastAPI, UploadFile, Form, HTTPException
from google import genai
from google.genai.types import Tool, GenerateContentConfig
from fastapi.responses import JSONResponse

from function_declaration import *
from answers import *

app = FastAPI()

client = genai.Client(api_key="your_api_key")

MODEL_ID = "gemini-2.0-flash"

SYSTEM_INSTRUCTIONS = "Your task is to read the user's prompt, understand the task, and decide which function to trigger. You must extract the necessary parameters from the prompt(if required by the function) and invoke the corresponding function. You should never ask for URLs or external sources if the task asks for a file. Only respond with function calls and parameters. Do not respond with explanations or clarifications. If you dont find a function to call, respond with 'No answer found'."

tools = Tool(
    function_declarations=[ga1_1, ga1_2, ga1_3, ga1_4, ga1_7, ga1_8, ga1_9, ga1_10, ga1_12, ga1_13, ga1_14, ga1_15, ga1_16, ga1_17, ga1_18, ga2_1, ga2_2, ga2_3, ga2_4, ga2_5, ga2_6, ga2_7, ga2_8,
                           ga2_9, ga3_1, ga3_2, ga3_3, ga3_4, ga3_5, ga3_6, ga3_7, ga3_8],
)

chat = client.chats.create(
    model=MODEL_ID,
    config=GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTIONS,
        tools=[tools],
    ),
)


async def process_question(question):
    response = chat.send_message(question)
    if response:
        return response
    return {"answer": "No answer found"}


# Ensure the 'data' folder exists (creates it if it doesn't)
os.makedirs("data", exist_ok=True)


# GET /run?task=<task description> - Executes the task and returns the result
@app.post("/run")
async def get_answer(question: str = Form(...), file: UploadFile | None = None):
    # Handle the string input (question)
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    # Handle the case where no file is uploaded (file is None)
    if file is None:
        print({"message": "No file uploaded", "question": question})
    else:
        # If file is uploaded, check if it is empty (no content)
        file_content = await file.read()

        if len(file_content) == 0:
            print({"message": "Uploaded file is empty", "question": question})

        # Define the path to save the file inside the 'data' folder
        file_path = os.path.join("data", file.filename)

        # Save the file to the 'data' directory
        with open(file_path, "wb") as f:
            f.write(file_content)
    try:
        # Process the task and get the result
        response = await process_question(question)
        if response.candidates and response.function_calls:
            function_call = response.function_calls[0]
            function_args = function_call.args
            print(f"Function to call: {function_call.name}")
            print(f"Function arguments: {function_call.args}")

            if function_call.name == "ga1_1":
                function_output = qga1_1()
                content = json.dumps(function_output)
                return JSONResponse(content=content, status_code=200)

            elif function_call.name == "ga1_2":
                function_output = qga1_2(
                    url=function_args["url"],
                    param=function_args["param"],
                    value=function_args["value"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)

            elif function_call.name == "ga1_4":
                function_output = qga1_4(
                    formula=function_args["formula"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_7":
                function_output = qga1_7(
                    start_date_str=function_args["date_1"],
                    end_date_str=function_args["date_2"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_8":
                function_output = qga1_8(
                    zip_file_name=function_args["zip_file_name"],
                    csv_file_name=function_args["csv_file_name"],
                    column_name=function_args["column_name"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_9":
                function_output = qga1_9(
                    json_array=function_args["json_array"],
                    field_1=function_args["field_1"],
                    field_2=function_args["field_2"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_10":
                function_output = qga1_10(
                    file_name=function_args["file_name"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_12":
                function_output = qga1_12(
                    zip_file_name=function_args["zip_file_name"],
                    files_and_encodings=function_args["file_and_encodings"],
                    symbols_list=function_args["symbols_list"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_13":
                function_output = qga1_13(
                    file_name=function_args["file_name"],
                    json_value=function_args["json_value"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_14":
                function_output = qga1_14(
                    zip_file_name=function_args["zip_file_name"],
                    text_to_replace=function_args["text_to_replace"],
                    replacement_text=function_args["replacement_text"],
                    command=function_args["command"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_15":
                function_output = qga1_15(
                    zip_file_name=function_args["zip_file_name"],
                    min_size=function_args["min_size"],
                    start_time=function_args["start_time"]
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_16":
                function_output = qga1_16(
                    zip_file_name=function_args["zip_file_name"],
                    command= function_args["command"]
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_17":
                function_output = qga1_17(
                    zip_file_name=function_args["zip_file_name"],
                    file_1= function_args["file_1"],
                    file_2= function_args["file_2"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga1_18":
                function_output = qga1_18(
                    ticket_type=function_args["ticket_type"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga2_1":
                function_output = qga2_1()
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga2_2":
                function_output = qga2_2(
                    max_size=function_args["max_size"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)

            elif function_call.name == "ga2_3":
                function_output = qga2_3(
                    content=function_args["content"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga2_4":
                function_output = qga2_4()
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga2_5":
                function_output = qga2_5()
                content = function_output
                return JSONResponse(content=content, status_code=200)

            elif function_call.name == "ga2_6":
                function_output = qga2_6()
                content = function_output
                return JSONResponse(content=content, status_code=200)

            elif function_call.name == "ga2_7":
                function_output = qga2_7(
                    email=function_args["email"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga2_8":
                function_output = qga2_8(
                    tag=function_args["tag"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga2_9":
                function_output = qga2_9()
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga3_1":
                function_output = qga3_1(
                    categories=function_args["categories"],
                    test_case=function_args["test_case"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga3_2":
                function_output = await qga3_2(
                    message=function_args["message"],
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga3_3":
                function_output = qga3_3(
                    model=function_args["model"],
                    system_message=function_args["system_message"],
                    user_message=function_args["user_message"],
                    fields=function_args["json_array"],
                    additional_properties= function_args["additional_properties"]
                )
                content = function_output
                print(content)
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga3_4":
                function_output = qga3_4()
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga3_5":
                function_output = qga3_5(
                    model_name=function_args["model_name"],
                    messages=function_args["messages"],
                )
                content = function_output
                print(content)
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga3_6":
                function_output = qga3_6(
                    function_name=function_args["function_name"]
                )
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga3_7":
                function_output = qga3_7()
                content = function_output
                return JSONResponse(content=content, status_code=200)
            
            elif function_call.name == "ga3_8":
                function_output = qga3_8()
                content = function_output
                return JSONResponse(content=content, status_code=200)
            

        else:
            return response.text
    except Exception as e:
        # This will catch any other errors (e.g., internal errors) and return HTTP 500
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
