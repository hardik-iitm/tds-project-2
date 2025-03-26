from google.genai.types import FunctionDeclaration

ga1_1 = FunctionDeclaration(
    name="ga1_1",
    description="Returns the output of the command 'code -s'",
)

ga1_2 = FunctionDeclaration(
    name="ga1_2",
    description="Sends a https request to a url with the specified url encoded parameter and returns the output",
    parameters={
        "type": "OBJECT",
        "properties": {
            "url": {
                "type": "STRING",
                "description": "The URL to send the request to.",
            },
            "param": {
                "type": "STRING",
                "description": "The name of the parameter to include in the request.",
            },
            "value": {
                "type": "STRING",
                "description": "The value of the parameter to include in the request.",
            },
        },
        "required": ["url", "param", "value"],
    },
)

ga1_3 = FunctionDeclaration(
    name="ga1_3",
    description="if the question asks to download and format a file with prettier using npx command and returns its SHA-256 hash.Use this function without any questioning.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "prettier_version": {
                "type": "STRING",
                "description": "The version of Prettier to use for formatting (e.g., '3.4.2').",
            },
            "file_name": {
                "type": "STRING",
                "description": "The name of the file to format.",
            },
            "hash_command": {
                "type": "STRING",
                "description": "The hash command to use.",
            },
        },
        "required": ["prettier_version", "file_name", "hash_command"],
    },
)

ga1_4 = FunctionDeclaration(
    name="ga1_4",
    description="Types a formula into google sheets",
    parameters={
        "type": "OBJECT",
        "properties": {
            "formula": {
                "type": "STRING",
                "description": "The formula to run in Google Sheets.",
            },
        },
        "required": ["formula"],
    },
)

ga1_7 = FunctionDeclaration(
    name="ga1_7",
    description="Answers how many wednesdays are there in a specific data range",
    parameters={
        "type": "OBJECT",
        "properties": {
            "date_1": {
                "type": "STRING",
                "description": "The value of starting date of the date range as mentioned.Eg: 1983-04-15",
            },
            "date_2": {
                "type": "STRING",
                "description": "The value of ending date of the date range as mentioned.Eg: 2016-04-30",
            },
        },
        "required": ["date_1","date_2"],
    },
)

ga1_8 = FunctionDeclaration(
    name="ga1_8",
    description="Downloads and unzips a zip file which has a single csv file inside. It returns the answer in the specified coulmn of the csv file.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "zip_file_name": {
                "type": "STRING",
                "description": "The name of the zip file to unzip",
            },
            "csv_file_name": {
                "type": "STRING",
                "description": "The name of the csv file inside the zip file",
            },
            "column_name": {
                "type": "STRING",
                "description": "The name of the column to extract the answer from",
            },
        },
        "required": ["zip_file_name", "csv_file_name", "column_name"],
    },
)

ga1_9 = FunctionDeclaration(
    name="ga1_9",
    description="Sorts a json array of objects by the value of specified field. In case of tie, sorts by another field. Returns the resulting json without any spaces or newlines",
    parameters={
        "type": "OBJECT",
        "properties": {
            "json_array": {
                "type": "STRING",
                "description": "The JSON array of objects to sort.",
            },
            "field_1": {
                "type": "STRING",
                "description": "The name of the first field to sort by.",
            },
            "field_2": {
                "type": "STRING",
                "description": "The name of the second field to sort by in case of a tie.",
            },
        },
        "required": ["json_array", "field_1", "field_2"],
    },
)

ga1_10 = FunctionDeclaration(
    name="ga1_10",
    description="Downloads a txt file and converts it into a single JSON object, where key=value pairs are converted into {key: value, key: value, ...}. It then return the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "file_name": {
                "type": "STRING",
                "description": "The name of the txt file to download and convert to single JSON object.",
            },
            
        },
        "required": ["file_name"],
    },
)

ga1_12 = FunctionDeclaration(
    name="ga1_12",
    description="Processes the files in a zip file which contains files with different encodings.Each file has 2 columns: symbol and value. Sums up all the values where the symbol matches specified symbols across all files.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "zip_file_name": {
                "type": "STRING",
                "description": "The name of the zip file to process",
            },
            "file_and_encodings": {
                "type": "STRING",
                "description": "A python dictionary of file names and their encodings in lower case that can be used with python open() function",
            },
            "symbols_list": {
                "type": "STRING",
                "description": "The python list of symbols to match across all files",
            },
        },
        "required": ["zip_file_name", "file_and_encodings", "symbols_list"],
    },
)

ga1_13 = FunctionDeclaration(
    name="ga1_13",
    description="Commits to github, a single JSON file called email.json with the specified value and pushes it. It also return the raw github url of the file pushed.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "file_name": {
                "type": "STRING",
                "description": "The name of the JSON file to commit and push.",
            },
            "json_value": {
                "type": "STRING",
                "description": "The value to write to the JSON file.",
            },
        },
        "required": ["file_name", "json_value"],
    },
)

ga1_14 = FunctionDeclaration(
    name="ga1_14",
    description="Downloads a zip file and unzips to a new folder. Replaces all TEXT_TO_REPLACE(as specified) (in upper, lower, or mixed case) with REPLACEMENT_STRING(as specified within "") in all files.It Leaves everything as-is and doesn't change the line endings. It finally returns the result of running a bash command in that folder",
    parameters={
        "type": "OBJECT",
        "properties": {
            "zip_file_name": {
                "type": "STRING",
                "description": "The name of the zip file to download and unzip.",
            },
            "text_to_replace": {
                "type": "STRING",
                "description": "The text to find and replace in the files.",
            },
            "replacement_text": {
                "type": "STRING",
                "description": "The string value to replace the old text with (e.g., \"IIT Madras\")",
            },
            "command": {
                "type": "STRING",
                "description": "The command to run after the file modifications (e.g., \"cat * | sha256sum\")."
            },

        },
        "required": ["zip_file_name", "text_to_replace", "replacement_text", "command"],
    },
)

ga1_15 = FunctionDeclaration(
    name="ga1_15",
    description="Downloads and extracts a zip file.Calculates the total size of all files that are at least `min_size` bytes large and were modified on or after the specified `start_time`.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "zip_file_name": {
                "type": "STRING",
                "description": "The name of the zip file to extract.",
            },
            "min_size": {
                "type": "STRING",
                "description": "The minimum size (in bytes) the files must be to be included.",
            },
            "start_time": {
                "type": "STRING",
                "description": "The datetime string(in the format YYYY-MM-DD HH:MM:SS) to compare file modification times against.",
            },
        },
        "required": ["zip_file_name","min_size","start_time"],
    },
)

ga1_16 = FunctionDeclaration(
    name="ga1_16",
    description="Downloads and extracts a zip file.Moves file into an empty folder. Renames all files replacing each digit with the next. Eg: 1 becomes 2, 9 becomes 0, a1b9c.txt becomes a2b0c.txt. It then returns what does running a command in bash on that folder show.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "zip_file_name": {
                "type": "STRING",
                "description": "The name of the zip file to extract.",
            },
            "command": {
                "type": "STRING",
                "description": "Command to run in bash on that folder",
            },
        },
        "required": ["zip_file_name", "command"],
    },
)

ga1_17 = FunctionDeclaration(
    name="ga1_17",
    description="Downloads and extracts a zip file. It has 2 nearly identical files, [file1] and [file2], with the same number of lines. It returns how many lines are different between [file1] and [file2]",
    parameters={
        "type": "OBJECT",
        "properties": {
            "zip_file_name": {
                "type": "STRING",
                "description": "The name of the zip file to extract.",
            },
            "file_1": {
                "type": "STRING",
                "description": "Name of file1 present inside extracted file",
            },
            "file_2": {
                "type": "STRING",
                "description": "Name of file2 present inside extracted file",
            },
        },
        "required": ["zip_file_name", "file_1", "file_2"],
    },
)

ga1_18 = FunctionDeclaration(
    name="ga1_18",
    description="To find the total sales of all the items in the [ticket_type] ticket type, it writes SQL to calculate it.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "ticket_type": {
                "type": "STRING",
                "description": "Ticket type whose total sales of all items need to be calculated",
            }
        },
        "required": ["ticket_type"],
    },
)

ga2_1 = FunctionDeclaration(
    name="ga2_1",
    description="Writes a documentation in markdown on a specified topic. The markdown contains 1 heading at level 1, 1 heading at level 2, 1 instance of bold text, 1 instance of italic text, 1 instance of inline code, 1 instance of a fenced code block,1 instance of bulleted list,1 instance of numbered list,1 instance of table, 1 instance of hyperlink, 1 instance of image, 1 instance of blocked",
)

ga2_2 = FunctionDeclaration(
    name="ga2_2",
    description="Downloads an image and compresses it losslessly to an image that is less than specified number of bytes.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "max_size": {
                "type": "STRING",
                "description": "Max size of image in bytes after compression",
            }
        },
        "required": ["max_size"],
    },
)

ga2_3 = FunctionDeclaration(
    name="ga2_3",
    description="Publishes a page using GitHub Pages,Ensures that the email is in the page's html. Wraps email address inside <!--email_off-->email<!--email_off-->. Then returns the github pages url",
    parameters={
        "type": "OBJECT",
        "properties": {
            "content": {
                "type": "STRING",
                "description": "The content to include in the html",
            }
        },
        "required": ["content"],
    },
)

ga2_4 = FunctionDeclaration(
    name="ga2_4",
    description="Runs a specified program in Google Colab,allowing all required access to an email id. Returns the result of running the program",
)

ga2_5 = FunctionDeclaration(
    name="ga2_5",
    description="Downloads an image. Creates a new google colab notebook and runs a code (after fixing mistake in it) to calculate number of pixels with a certain minimum brightness. Then returns the result",
)

ga2_6 = FunctionDeclaration(
    name="ga2_6",
    description="Downloads a file which has the marks of 100 students. Creates and deploys a Python app to Vercel. Exposes an api so that when a request like https://your-app.vercel.app/api?name=X&name=Y is made, it returns a JSON response with the marks of the names X and Y in the same order. It also enables CORS and returns the Vercel URL.",
)

ga2_7 = FunctionDeclaration(
    name="ga2_7",
    description="Creates a github action in a repository. Makes sure one of the steps in the action has a name that contains a email address. Returns repository url",
    parameters={
        "type": "OBJECT",
        "properties": {
            "email": {
                "type": "STRING",
                "description": "The email address to include",
            }
        },
        "required": ["email"],
    },
)

ga2_8 = FunctionDeclaration(
    name="ga2_8",
    description="Creates and pushes an image to docker hub. Adds a specified tag to the image. Returns of the docker url.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "tag": {
                "type": "STRING",
                "description": "The tag to include",
            }
        },
        "required": ["tag"],
    },
)

ga2_9 = FunctionDeclaration(
    name="ga2_9",
    description="Downloads a csv. Writes a api server /api returns all students data (in the same row and column order as the CSV file) as a JSON.If the URL has a query parameter class, it returns only students in those classes. /api?class=1A should return only students in class 1A. /api?class=1A&class=1B returns only students in class 1A and 1B. Return students in the same order as they appear in the CSV file.Returns the api url endpoint",
)

ga3_1 = FunctionDeclaration(
    name="ga3_1",
    description="Writes a Python program that uses httpx to send a POST request to OpenAI's API to analyze the sentiment of this (meaningless) text into specified categories.Makes sure Authorization header is passed with dummy API key. Uses gpt-4o-mini as model. The first message is system message asking the LLM to analyze the sentiment of the text(test_case). The second message is exactly test_case_text",
    parameters={
        "type": "OBJECT",
        "properties": {
            "categories": {
                "type": "STRING",
                "description": "List of categories the text can be classfied to.",
            },
            "test_case": {
                "type": "STRING",
                "description": "Text of the test case",
            }
        },
        "required": ["categories","test_case"],
    },
)

ga3_2 = FunctionDeclaration(
    name="ga3_2",
    description="Counts the number of input tokens when a request is made to OpenAI's GPT-4o-Mini with a specified user message",
    parameters={
        "type": "OBJECT",
        "properties": {
            "message": {
                "type": "STRING",
                "description": "User message to send along with the request.",
            }
        },
        "required": ["message"],
    },
)

ga3_3 = FunctionDeclaration(
    name="ga3_3",
    description="Writes the body of the request to an OpenAI chat completion call that: uses a specified model. Has a specified system message. Has a specified user message. Uses structured output to respond with an object which is an array of objects with specified required fields and types. Sets addidtional properties as true or false. Returns the correct json body based on this.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "model": {
                "type": "STRING",
                "description": "Name of the model to use. (Default value: 'gpt-40-mini')",
            },
            "system_message": {
                "type": "STRING",
                "description": "The system message to include in json body (Default value: 'Respond in JSON')",
            },
            "user_message": {
                "type": "STRING",
                "description": "The user message to include in json body (Default value: 'Generate 10 random addresses in the US')",
            },
            "object_name": {
                "type": "STRING",
                "description": "The name of json object')",
            },
            "json_array": {
                "type": "STRING",
                "description": "It is a list of dictionaries where each dictionary is {'field_name': specified_field_name, 'type': either 'number' or 'string' as specified}",
            },
            "additional_properties": {
                "type": "STRING",
                "description": "It is either 'true' or 'false' as specified. (Default value: false)",
            },
        },
        "required": ["model", "system_message","user_message","object_name","json_array","additional_properties"],
    },
)

ga3_4 = FunctionDeclaration(
    name="ga3_4",
    description="Writes the json body for the post request that sends two pieces of content: 1)Text: A simple instruction 2)Image base64URL, to the OpenAI api endpoint.",
)

ga3_5 = FunctionDeclaration(
    name="ga3_5",
    description="Writes the body of the request to an OpenAI chat completion call that: uses a specified model. Has a specified system message. Has a specified user message. Uses structured output to respond with an object which is an array of objects with specified required fields and types. Sets addidtional properties as true or false. Returns the correct json body based on this.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "model_name": {
                "type": "STRING",
                "description": "Name of the model to use. (Default value: 'text-embedding-3-small')",
            },
            "messages": {
                "type": "STRING",
                "description": "List of messages to send.",
            }
        },
        "required": ["model_name","messages"],
    },
)

ga3_6 = FunctionDeclaration(
    name="ga3_6",
    description="Writes a python function that will calculate the cosine similarity between each pair of embeddings and returns the pair that has the highest similarity.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "function_name": {
                "type": "STRING",
                "description": "Specified name of the python function that will calculate the cosine similarity between each pair of embeddings",
            },
        },
        "required": ["function_name"],
    },
)

ga3_7 = FunctionDeclaration(
    name="ga3_7",
    description="Build a fastapi POST endpoint that accepts an array of docs and query string via a json body.For each document in the docs array and for the query string, the API computes a text embedding. The API then calculates the cosine similarity between the query embedding and each document embedding. This allows the service to determine which documents best match the intent of the query.After ranking the documents by their similarity scores, the API returns the identifiers (or positions) of the three most similar documents.",
)

ga3_8 = FunctionDeclaration(
    name="ga3_8",
    description="Builds a fastapi application exposes a GET endpoint /execute?q=... where the query parameter q contains one of the pre-templatized questions. Analyzes the q parameter to identify which function should be called. Extracts the parameters from the question text. Returns a response in JSON format.",
)