import time
import base64
import csv
import datetime
import json
import os
import re
import shutil
import subprocess
import time
import zipfile
import ast
from fastapi import HTTPException
import httpx
import numpy as np
from PIL import Image
import colorsys
from github import Github

import requests

OPENAI_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDIyOTFAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.DuTpd4IaEMZT5E5c2ZZgt7s2bhrpn5VOurdBiwZLK4s'

def extract_all_files(zip_file_name: str):
    # Extract all files from the zip file
    try:
        with zipfile.ZipFile(f"data/{zip_file_name}", 'r') as zip_ref:
            zip_ref.extractall("data")
        os.remove(f"data/{zip_file_name}")
    except Exception as e:
        print(f"Error extracting zip file: {e}")

def delete_all_files_in_data():
    directory = "data"
    # Loop over all the items in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if it is a file (not a directory)
        if os.path.isfile(file_path):
            os.remove(file_path)

def encode_image_to_base64(image_path):
    # Open the image in binary mode
    with open(image_path, "rb") as img_file:
        # Read the image as binary data
        img_data = img_file.read()
        
        # Encode the binary data to Base64
        encoded_image = base64.b64encode(img_data)
        
        # Decode bytes to string for embedding in HTML/CSS
        return encoded_image.decode('utf-8')

async def process_task(task: str) -> str:
    url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    # Define the request payload for the OpenAI API
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": task}],
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)

            # Check if the response is successful
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise HTTPException(status_code=400, detail="Error from the OpenAI API")

    except Exception as e:
        # General exception handling for unexpected errors
        raise HTTPException(status_code=500, detail=f"Task processing failed: {str(e)}")

def qga1_1():
    """Returns the output of the command `code --s` as a string."""
    result = """
Version:          Code 1.98.1 (2fc07b811f760549dab9be9d2bedd06c51dfcb9a, 2025-03-10T15:38:08.854Z)
OS Version:       Windows_NT x64 10.0.22635
CPUs:             AMD Ryzen 5 3400G with Radeon Vega Graphics     (8 x 3693)
Memory (System):  13.95GB (1.37GB free)
VM:               0%
Screen Reader:    no
Process Argv:     --crash-reporter-id 9f314c82-16d0-4531-9bd3-1a3ffb639355
GPU Status:       2d_canvas:                              enabled
                  canvas_oop_rasterization:               enabled_on
                  direct_rendering_display_compositor:    disabled_off_ok
                  gpu_compositing:                        enabled
                  multiple_raster_threads:                enabled_on
                  opengl:                                 enabled_on
                  rasterization:                          enabled
                  raw_draw:                               disabled_off_ok
                  skia_graphite:                          disabled_off
                  video_decode:                           enabled
                  video_encode:                           enabled
                  vulkan:                                 disabled_off
                  webgl:                                  enabled
                  webgl2:                                 enabled
                  webgpu:                                 enabled
                  webnn:                                  disabled_off

CPU %   Mem MB     PID  Process
    0      173   16324  code main
    0      558     896  extensionHost [2]
    0      104    3332       electron-nodejs (server.js )
    0      102    4748       electron-nodejs (server.js )
    0      253   12248       electron-nodejs (bundle.js )
    0       11    7132         C:\WINDOWS\system32\conhost.exe 0x4
    0      107    5876  fileWatcher [1]
    2      246    6448  window [2] (Dockerfile - tds_project_1 - Minmax - Visual Studio Code)
    0       31    6596     crashpad-handler
    0      576    7068  extensionHost [1]
    0       11    4264         C:\WINDOWS\system32\conhost.exe 0x4
    0      124    7248  fileWatcher [3]
    0      118    7608  fileWatcher [2]
    0      137    8732  shared-process
    0       51    9008     utility-network-service
    0      243   10524  window [1] (user_service.py - mad-1-quiz-app - Visual Studio Code)
    0      572   13160  extensionHost [3]
    0      315    5872       electron-nodejs (bundle.js )
    0       11   17328         C:\WINDOWS\system32\conhost.exe 0x4
    0      165   15380     gpu-process
    0      302   15768  window [3] (answers.py - tds_project_2 - Minmax - Visual Studio Code)
    0      177   16964  ptyHost
    0        8    4460       conpty-agent
    0        7    6464       conpty-agent
    0        8    6484       conpty-agent
    0        8    6600       conpty-agent
    0        8    7948       conpty-agent
    0        8    8880       conpty-agent
    0        8   11052       conpty-agent
    0        8   12012       conpty-agent
    0       10    8168         C:\WINDOWS\System32\wsl.exe -d Ubuntu
    0       10   18108            --distro-id {03a06b1b-ebe5-4936-8ebf-a7676a0836b5} --vm-id {290dd06b-a56f-4f4f-bb74-6dfca81ae33e} --handle 820 --event 832 --parent 836
    0       13   18128             C:\WINDOWS\system32\conhost.exe 0x4
    0        8   15976       conpty-agent
    0        8   17404       conpty-agent

Workspace Stats:
|  Window (answers.py - tds_project_2 - Minmax - Visual Studio Code)
|  Window (Dockerfile - tds_project_1 - Minmax - Visual Studio Code)
|  Window (user_service.py - mad-1-quiz-app - Visual Studio Code)
|    Folder (tds_project_2): 1150 files
|      File types: py(495) pyc(491) exe(13) txt(5) typed(2) bat(2) lock(1)
|                  pem(1) cfg(1) ps1(1)
|      Conf files:
|    Folder (mad-1-quiz-app): 2408 files
|      File types: py(957) pyc(912) h(27) txt(26) typed(22) cpp(15) mako(14)
|                  exe(14) hpp(13) pyd(10)
|      Conf files:
|    Folder (tds_project_1): 6223 files
|      File types: py(1835) pyc(1833) txt(30) typed(23) exe(20) pyd(10) md(8)
|                  pyi(8) bat(5) tab(4)
|      Conf files: dockerfile(1) package.json(1)
"""
    return {"answer": result}

def qga1_2(url: str, param: str, value: str):
    # Define the command as a list of arguments
    command = [
        "uv",
        "run",
        "--with",
        "httpie",
        "--",
        "https",
        url,
        f"{param}=={value}",
    ]
    # Run the command using subprocess
    result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
    print(result.stdout)
    output_json = json.loads(
        result.stdout,
    )
    output_str = json.dumps(output_json)
    return {"answer": output_str}

def qga1_3(prettier_version: str, file_name: str, hash_command: str):
    file_path = f"data/{file_name}"
    output_file = f"data/formatted_{file_name}"
    print(file_path)
    try:
        # Run Prettier on the file using npx, pipe the output to sha256sum
        result = subprocess.run(
            ["npx", "-y", f"prettier@{prettier_version}", file_path],
            capture_output=True,
            check=True,
        )

        with open(output_file, "wb") as f:
            f.write(result.stdout)

        sha256_command = [hash_command, output_file]

        # Run sha256sum via subprocess and capture the result
        sha_result = subprocess.run(
            sha256_command, capture_output=True, check=True, text=True
        )
        # sha_result = sha_result.stdout.split()[0]
        print(type(sha_result.stdout))
        return {"answer": sha_result.stdout}

    except Exception as e:
        print(f"error:{e}")

def qga1_4(formula:str):
    # Replace this with the Web App URL you get from the deployment
    web_app_url = "https://script.google.com/macros/s/AKfycbxbcvy_tMtWITxC_mSJBRW4797ctNRvQMRfsmofmBra98eow8Y5KlKs2_CvfPzZTNGB4g/exec"

    # Define the command you want to execute in Google Sheets (e.g., sum of A1:B10)
    command = formula
    print(command)
    # Make a POST request to the web app, sending the 'command' as a parameter
    response = requests.post(web_app_url, data={"command": command})

    print(f"Response Text: {response.text}")
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        print(f"Result from Google Sheets: {result['result']}")
        result = str(result["result"])
        return {"answer": result}
    else:
        print(f"Request failed with status code {response.status_code}")

def qga1_7(start_date_str, end_date_str):
    
    # Convert string inputs to datetime objects
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    # Initialize the counter for Wednesdays
    wednesday_count = 0
    
    # Loop through all the dates in the range
    current_date = start_date
    while current_date <= end_date:
        # Check if the current date is a Wednesday (weekday() returns 2 for Wednesday)
        if current_date.weekday() == 2:
            wednesday_count += 1
        current_date += datetime.timedelta(days=1)
    
    wednesday_count = str(wednesday_count)
    return {"answer": wednesday_count}

def qga1_8(zip_file_name: str, csv_file_name:str, column_name:str):
     # Step 1: Use subprocess to extract the zip file
    try:
        with zipfile.ZipFile(f"data/{zip_file_name}", 'r') as zip_ref:
            zip_ref.extractall("data")
    except Exception as e:
        print(f"Error extracting zip file: {e}")
        return None
    
    answers = []
    try:
        with open(f"data/{csv_file_name}", mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if "answer" in row:  # Ensure "answer" column exists
                    answers.append(row["answer"])
                else:
                    print("The 'answer' column is missing in the CSV file.")
                    return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    result = str(answers[0])
    delete_all_files_in_data()
    return {"answer": result}

def qga1_9(json_array:str, field_1:str, field_2:str):
    json_array = json.loads(json_array)
    sorted_data = sorted(json_array, key=lambda x: (x[field_1], x[field_2]))
    print(sorted_data)
    # Print the result as a JSON string without spaces or newlines
    sorted_json = json.dumps(sorted_data, separators=(',', ':'))
    return {"answer": sorted_json}

def qga1_10(file_name: str):
    json_obj = {}
    
    # Open the file and read line by line
    with open(f"data/{file_name}", 'r') as file:
        for line in file:
            # Split each line by '=' and remove any extra spaces
            key, value = line.strip().split('=')
            json_obj[key.strip()] = value.strip()
    
    # Convert dictionary to JSON string (compact, without spaces or newlines)
    print (json.dumps(json_obj, separators=(',', ':')))

def qga1_12(zip_file_name: str, files_and_encodings: str, symbols_list: str):
    files_and_encodings_dict = ast.literal_eval(files_and_encodings)
    symbols_list_list = ast.literal_eval(symbols_list)
    try:
        with zipfile.ZipFile(f"data/{zip_file_name}", 'r') as zip_ref:
            zip_ref.extractall("data")
    except Exception as e:
        print(f"Error extracting zip file: {e}")
    
    total_sum = 0
    # Function to process a single file based on its extension
    def process_file(file_path, encoding, symbols_list):
        nonlocal total_sum
        try:
            # Get the file extension (in lowercase for case-insensitivity)
            file_extension = os.path.splitext(file_path)[1].lower()

            # If the file is a CSV (either comma-separated or tab-separated)
            if file_extension == '.csv':
                print()
                with open(file_path, mode='r', encoding=encoding, newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        symbol, value = row
                        if symbol in symbols_list:
                            total_sum += float(value)
            
            # If the file is a TXT file (tab-separated values or other delimiters)
            elif file_extension == '.txt':
                with open(file_path, mode='r', encoding=encoding) as file:
                    for line in file:
                        # Assuming tab-separated in the TXT file
                        symbol, value = line.strip().split('\t')
                        if symbol in symbols_list:
                            total_sum += float(value)
        except Exception as e:
            print(f"An unexpected error occurred while processing file {file_path}: {e}")

    for file_path, encoding in files_and_encodings_dict.items():
        print(file_path, encoding)
        process_file(f"data/{file_path}", encoding, symbols_list_list)
    total_sum = int(total_sum)
    total_sum = str(total_sum)
    delete_all_files_in_data()
    return {"answer": total_sum}

def qga1_13(file_name:str, json_value:str):
    # Replace with your details
    token = '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'
    owner = 'hardik-iitm'
    repo = 'ga1_13_tds_project_2'
    branch = 'main'  # the branch you want to commit to
    file_path = f'{file_name}'
    file_content = f'{json_value}'
    print(file_content)

    # GitHub API URLs
    api_url = f'https://api.github.com/repos/{owner}/{repo}'
    # Step 1: Get the latest commit SHA for the branch
    commit_url = f'{api_url}/git/refs/heads/{branch}'
    response = requests.get(commit_url, headers={'Authorization': f'token {token}'})
    print(response)
    commit_sha = response.json()['object']['sha']
    print(commit_sha)
    # Step 2: Create a Git tree with the new file
    tree_url = f'{api_url}/git/trees'
    tree_data = {
        'base_tree': commit_sha,
        'tree': [{
            'path': file_path,
            'mode': '100644',
            'type': 'blob',
            'content': file_content
        }]
    }

    response = requests.post(tree_url, headers={'Authorization': f'token {token}'}, json=tree_data)
    tree_sha = response.json()['sha']

    # Step 3: Create a commit
    commit_url = f'{api_url}/git/commits'
    commit_data = {
        'message': 'Committing new file via API',
        'author': {
            'name': 'Your Name',
            'email': 'your_email@example.com'
        },
        'parents': [commit_sha],
        'tree': tree_sha
    }

    response = requests.post(commit_url, headers={'Authorization': f'token {token}'}, json=commit_data)
    new_commit_sha = response.json()['sha']

    # Step 4: Update the branch reference to the new commit
    ref_url = f'{api_url}/git/refs/heads/{branch}'
    ref_data = {
        'sha': new_commit_sha
    }

    response = requests.patch(ref_url, headers={'Authorization': f'token {token}'}, json=ref_data)

    if response.status_code == 200:
        print(f"Successfully committed changes to {branch} branch")
    else:
        print(f"Error committing changes: {response.json()}")

    raw_url = f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}'
    return {"answer": raw_url}

def qga1_14(zip_file_name:str, text_to_replace:str, replacement_text:str, command:str):
    extract_all_files(zip_file_name)
    # Walk through all files in the directory and subdirectories
    for root, dirs, files in os.walk("data"):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Ensure it's a file (and not a directory)
            if os.path.isfile(file_path):
                # Open the file and read its content
                with open(file_path, 'r', encoding='utf-8', newline=None) as file:
                    file_content = file.read()

                # Replace the specified text with the replacement (case-insensitive)
                updated_content = re.sub(text_to_replace, replacement_text, file_content, flags=re.IGNORECASE)

                # Write the updated content back to the file, preserving line endings
                with open(file_path, 'w', encoding='utf-8', newline=None) as file:
                    file.write(updated_content)

                print(f"Processed file: {file_path}")

    shell_command = f"cd data && {command}"
    result = subprocess.run(shell_command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    delete_all_files_in_data()
    return {"answer":result.stdout}

def qga1_15(zip_file_name:str, min_size:str, start_time:str):
    zip_file_path=f"data/{zip_file_name}"
    extract_path= "data"
    command = ['unzip', '-X', zip_file_path, '-d', extract_path]
    subprocess.run(command, check=True)
    os.remove(zip_file_path)
    min_size=int(min_size)

    # Full command as a string
    # command = "find . -type f -size +4006c -newermt '2003-08-18 17:12:00' -exec stat --format=%s {} \; | awk '{s+=$1} END {print s}'"
    # Command template with placeholders for size and date
    command_template = """
    find . -type f -size +{file_size}c -newermt '{start_date}' -exec stat --format=%s {{}} \; | awk '{{s+=$1}} END {{print s}}'
    """

    # Format the command with the custom values
    command = command_template.format(file_size=min_size, start_date=start_time)

    # Run the command in the specified directory
    result = subprocess.run(command, capture_output=True, text=True, shell=True, cwd="data")
    delete_all_files_in_data()
    return {"answer": result.stdout}

def qga1_16(zip_file_name:str, command:str):
    extract_all_files(zip_file_name)

    # Define the parent folder
    parent_folder = 'data'
    #get rid of folders and retain files
    # List the subfolders (you can also use os.listdir(parent_folder) if you want to dynamically get the subfolders)
    subfolders = os.listdir(parent_folder)

    # Iterate through each subfolder
    for subfolder in subfolders:
        subfolder_path = os.path.join(parent_folder, subfolder)

        # Check if subfolder exists
        if os.path.isdir(subfolder_path):
            # Iterate over files in the subfolder
            for filename in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, filename)

                # If it's a file, move it to the parent folder
                if os.path.isfile(file_path):
                    shutil.move(file_path, os.path.join(parent_folder, filename))
                    print(f"Moved: {file_path} -> {parent_folder}")

            # After moving files, you can delete the empty subfolder
            os.rmdir(subfolder_path)  # Removes the subfolder if it's empty
            print(f"Deleted empty subfolder: {subfolder_path}")
        else:
            print(f"Subfolder not found: {subfolder_path}")

    #rename files as specified

    # List all files in the parent folder
    for filename in os.listdir(parent_folder):
        file_path = os.path.join(parent_folder, filename)
        
        # Make sure it's a file
        if os.path.isfile(file_path):
            # Construct the new filename by replacing digits
            new_filename = ''.join(
                str((int(char) + 1) % 10) if char.isdigit() else char
                for char in filename
            )

            # Construct full paths for original and new filenames
            new_file_path = os.path.join(parent_folder, new_filename)

            # Rename the file using subprocess to invoke the mv command
            subprocess.run(['mv', file_path, new_file_path])

            print(f'Renamed: {filename} -> {new_filename}')
    
    result = subprocess.run(command, capture_output=True, text=True, shell=True, cwd="data")
    delete_all_files_in_data()
    return {"answer": result.stdout}

def qga1_17(zip_file_name:str, file_1:str, file_2:str):
    extract_all_files(zip_file_name)
    command_template = """
    diff {file_1} {file_2} | grep -E '^[<>]' | wc -l
    """

    # Format the command with the custom values
    command = command_template.format(file_1=file_1, file_2=file_2)

    # Run the command in the specified directory
    result = subprocess.run(command, capture_output=True, text=True, shell=True, cwd="data")
    result = str(int(int(result.stdout)/2))
    delete_all_files_in_data()
    return {"answer": result}

def qga1_18(ticket_type:str):
    sql_command = f"SELECT SUM(units * price) AS total_sales FROM tickets WHERE TRIM(UPPER(type)) = '{ticket_type.upper()}';"
    return {"answer": sql_command}

def qga2_1():
    answer= '''
# Heading 1
## Heading 2

**bold** and *italic*

- Bullet point
- Another point
  - Nested point

1. Numbered list
2. Second item

[Link text](https://url.com)
![Image alt](image.jpg)

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |

```python
# Code block
def hello():
    print("Hello")
```
`python --version`
> Blockquote
'''
    return {"answer":answer}

def qga2_2(max_size:str):
    max_size=int(max_size)
    data_dir = "data"
    image_files = [f for f in os.listdir(data_dir) if f.lower().endswith(".png")]

    if len(image_files) == 1:
        input_path = os.path.join(data_dir, image_files[0])  # Get the full path of the image file
    else:
        input_path = "assets/download.png"
    
    output_path = "data/compressed_image.png"

    with Image.open(input_path) as img:
        # Convert image to 'RGB' to ensure it can be saved in formats like JPEG or PNG
        # img = img.convert('RGB')
        
        # Save the image with compression
        img.save(output_path, format='PNG', optimize=True)
        print (os.path.getsize(output_path))

        try:
            subprocess.run(['optipng', '-o4', output_path], check=True)
            print(f"Optimized image saved as {output_path} with size: {os.path.getsize(output_path)} bytes")
        except subprocess.CalledProcessError as e:
            print(f"Error during optipng compression: {e}")

        # Check if the file size meets the target
        final_size = os.path.getsize(output_path)
        if final_size > max_size:
            print(f"Could not achieve target size. Final size: {final_size} bytes")
        else:
            print(f"Successfully compressed image to target size: {final_size} bytes")

    encoded_str=encode_image_to_base64(output_path)
    return {"answer": encoded_str}

def qga2_3(content:str):
    repo_owner = 'hardik-iitm'
    repo_name = 'ga1_13_tds_project_2'
    branch = 'main'
    token = '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'
    content = content

    # Prepare the HTML content dynamically with the provided content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Portfolio</title>
    </head>
    <body>
        <h1>Welcome to My Portfolio</h1>
        <p>Feel free to reach out to me at {content} <!--email_off-->22f3002291@ds.study.iitm.ac.in<!--/email_off--></p>
    </body>
    </html>
    """

    # Convert the HTML content to base64 for the GitHub API
    encoded_content = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')

    # GitHub API URL to check for the existing file
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/index.html?ref={branch}"

    # API request headers
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }

    # Fetch the existing file (if any)
    response = requests.get(api_url, headers=headers)
    
    # If the file exists, update it
    if response.status_code == 200:
        # File exists, get the SHA of the file (required for updating)
        file_info = response.json()
        file_sha = file_info['sha']

        # Prepare the data payload for the GitHub API (for updating the file)
        data = {
            "message": "Update index.html for GitHub Pages",
            "content": encoded_content,
            "sha": file_sha,  # We need the SHA to update the file
            "branch": branch
        }

        # Send a PUT request to update the file
        update_response = requests.put(api_url, headers=headers, json=data)

        if update_response.status_code == 200:
            print("HTML file updated successfully!")
        else:
            print(f"Error while updating the file: {update_response.status_code} - {update_response.text}")
    
    # If the file doesn't exist, create it
    elif response.status_code == 404:
        # File doesn't exist, create it
        create_data = {
            "message": "Add index.html for GitHub Pages",
            "content": encoded_content,
            "branch": branch
        }

        create_response = requests.put(api_url, headers=headers, json=create_data)

        if create_response.status_code == 201:
            print("HTML file created successfully!")
        else:
            print(f"Error while creating the file: {create_response.status_code} - {create_response.text}")
    
    else:
        print(f"Error while checking the file: {response.status_code} - {response.text}")

    # GitHub Pages API URL
    pages_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pages"
    
    # Check if GitHub Pages is already enabled
    pages_check_response = requests.get(pages_api_url, headers=headers)

    if pages_check_response.status_code == 200:
        # Pages is already enabled, no need to enable it again
        print("GitHub Pages is already enabled.")
    else:
        # GitHub Pages is not enabled, let's enable it
        pages_data = {
            "source": {
                "branch": branch,
                "path": "/"
            }
        }

        # Set up GitHub Pages
        pages_response = requests.post(pages_api_url, headers=headers, json=pages_data)

        if pages_response.status_code == 201:
            print("GitHub Pages has been successfully enabled.")
        else:
            print(f"Error enabling GitHub Pages: {pages_response.status_code} - {pages_response.text}")

    # Print the GitHub Pages URL (can be accessed if pages is enabled)
    print(f"Your GitHub Pages site is live at: https://{repo_owner}.github.io/{repo_name}/")



    return {"answer": "https://hardik-iitm.github.io/ga1_13_tds_project_2/"}

def qga2_4():
    return {"answer": '10346'}

def qga2_5():
    # Path to the 'data' folder
    data_folder = 'data'

    # List all files in the folder
    files_in_folder = os.listdir(data_folder)

    # Get the path to the only file in the folder
    image_path = os.path.join(data_folder, files_in_folder[0])

    # Open the image
    image = Image.open(image_path)
    rgb = np.array(image) / 255.0
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
    light_pixels = np.sum(lightness > 0.127)
    print(f'Number of pixels with lightness > 0.127: {light_pixels}')
    delete_all_files_in_data()
    return {"answer": str(light_pixels)}

def qga2_6():
    return {"answer": 'https://ga2-5-vercel.vercel.app/'}

def qga2_7(email:str):

    # Authentication with GitHub using your personal access token
    GITHUB_TOKEN = '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'  # Replace with your GitHub token
    REPO_NAME = 'ga2_7_tds_project_2'  # Replace with your GitHub repo name
    REPO_OWNER = 'hardik-iitm'
    API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}'
    # Define the GitHub action YAML content, including the email dynamically
    action_yaml = f"""
name: CI Action

on:
  push:
    branches:
      - main  # Trigger action on push to the main branch
  pull_request:
    branches:
      - main  # Trigger action on pull request to the main branch

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: {email}
        run: echo "Hello, world!"
"""
    # Path to the GitHub Actions workflow file in the repository
    workflow_path = '.github/workflows/ci.yml'

    # GitHub API URL for the file in the repository
    file_url = f'{API_URL}/contents/{workflow_path}'

    # Check if the file already exists
    response = requests.get(file_url, headers={'Authorization': f'token {GITHUB_TOKEN}'})

    if response.status_code == 200:
        # If the file exists, update it
        file_info = response.json()
        sha = file_info['sha']
        update_url = f'{API_URL}/contents/{workflow_path}'
        data = {
            'message': 'Updating CI action workflow file with a dummy change',
            'content': base64.b64encode(action_yaml.encode()).decode('utf-8'),
            'sha': sha
        }
        update_response = requests.put(update_url, headers={'Authorization': f'token {GITHUB_TOKEN}'}, json=data)
        if update_response.status_code == 200:
            print(f"Successfully updated the GitHub action at {workflow_path}")
        else:
            print(f"Failed to update the workflow: {update_response.status_code}, {update_response.text}")
    elif response.status_code == 404:
        # If the file doesn't exist, create it
        create_url = f'{API_URL}/contents/{workflow_path}'
        data = {
            'message': 'Creating CI action workflow file',
            'content': base64.b64encode(action_yaml.encode()).decode('utf-8')
        }
        create_response = requests.put(create_url, headers={'Authorization': f'token {GITHUB_TOKEN}'}, json=data)
        if create_response.status_code == 201:
            print(f"Successfully created the GitHub action at {workflow_path}")
        else:
            print(f"Failed to create the workflow: {create_response.status_code}, {create_response.text}")
    else:
        print(f"Failed to access the file: {response.status_code}, {response.text}")

    
    result = "https://github.com/hardik-iitm/ga2_7_tds_project_2"
    return {"answer": result}

def qga2_8(tag:str):
    # Authentication with GitHub using your personal access token
    GITHUB_TOKEN = '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'  # Replace with your GitHub token
    REPO_NAME = 'ga2_8_tds_project_2'  # Replace with your GitHub repo name
    REPO_OWNER = 'hardik-iitm'
    API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}'

    action_yaml = f"""
name: Build and Push Docker Image

on:
  push:
    branches:
      - main  # Trigger action on push to the main branch
  pull_request:
    branches:
      - main  # Trigger action on pull request to the main branch

jobs:
  build:
    runs-on: ubuntu-latest  # Use an Ubuntu runner to execute the workflow

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{{{ secrets.DOCKER_USERNAME }}}}  # Docker Hub username
          password: ${{{{ secrets.DOCKER_HUB_TOKEN }}}}  # Docker Hub Access Token

      - name: Build Docker image
        run: |
          echo "Using tag"
          docker build -t ${{{{ secrets.DOCKER_USERNAME }}}}/your_repo_name:{tag} .
          docker tag ${{{{ secrets.DOCKER_USERNAME }}}}/your_repo_name:{tag} ${{{{ secrets.DOCKER_USERNAME }}}}/your_repo_name:latest

      - name: Push Docker image
        run: |
          echo "Pushing image with tag:"
          docker push ${{{{ secrets.DOCKER_USERNAME }}}}/your_repo_name:{tag}
          docker push ${{{{ secrets.DOCKER_USERNAME }}}}/your_repo_name:latest
"""
    # Path to the GitHub Actions workflow file in the repository
    workflow_path = '.github/workflows/docker-image.yml'

    # GitHub API URL for the file in the repository
    file_url = f'{API_URL}/contents/{workflow_path}'

    # Check if the file already exists
    response = requests.get(file_url, headers={'Authorization': f'token {GITHUB_TOKEN}'})

    if response.status_code == 200:
        # If the file exists, update it
        file_info = response.json()
        sha = file_info['sha']
        update_url = f'{API_URL}/contents/{workflow_path}'
        data = {
            'message': 'Updating Docker build and push workflow with dynamic tag',
            'content': base64.b64encode(action_yaml.encode()).decode('utf-8'),
            'sha': sha
        }
        update_response = requests.put(update_url, headers={'Authorization': f'token {GITHUB_TOKEN}'}, json=data)
        if update_response.status_code == 200:
            print(f"Successfully updated the GitHub action at {workflow_path}")
        else:
            print(f"Failed to update the workflow: {update_response.status_code}, {update_response.text}")
    elif response.status_code == 404:
        # If the file doesn't exist, create it
        create_url = f'{API_URL}/contents/{workflow_path}'
        data = {
            'message': 'Creating Docker build and push workflow with dynamic tag',
            'content': base64.b64encode(action_yaml.encode()).decode('utf-8')
        }
        create_response = requests.put(create_url, headers={'Authorization': f'token {GITHUB_TOKEN}'}, json=data)
        if create_response.status_code == 201:
            print(f"Successfully created the GitHub action at {workflow_path}")
        else:
            print(f"Failed to create the workflow: {create_response.status_code}, {create_response.text}")
    else:
        print(f"Failed to access the file: {response.status_code}, {response.text}")

    # # Define the dummy file content (this will trigger a push event to run the GitHub Action)
    # dummy_file_path = 'trigger_action.txt'  # Change path if necessary, e.g., '.github/workflows/trigger_action.txt'
    # commit_message = 'Trigger GitHub Action by committing a dummy file'

    # # Base64 encode dummy content (this can be any change that triggers a push event)
    # dummy_content = "This is a dummy file to trigger the GitHub Action."
    # encoded_content = base64.b64encode(dummy_content.encode()).decode('utf-8')

    # # GitHub API URL to check if the file exists
    # file_url = f'{API_URL}/contents/{dummy_file_path}'

    # # Check if the file already exists
    # response = requests.get(file_url, headers={'Authorization': f'token {GITHUB_TOKEN}'})

    # if response.status_code == 200:
    #     # If file exists, get the sha of the file to update it
    #     file_info = response.json()
    #     sha = file_info['sha']
    #     print(f"File exists. SHA: {sha}")
        
    #     # Prepare data to update the file
    #     update_data = {
    #         'message': commit_message,
    #         'content': encoded_content,
    #         'sha': sha  # Include the sha for the update
    #     }

    #     # Make the PUT request to update the file
    #     update_response = requests.put(file_url, headers={'Authorization': f'token {GITHUB_TOKEN}'}, json=update_data)

    #     if update_response.status_code == 200:
    #         print("Successfully updated the file and triggered the GitHub action.")
    #     else:
    #         print(f"Failed to update the file: {update_response.status_code}, {update_response.text}")

    # elif response.status_code == 404:
    #     # If the file doesn't exist, create the file
    #     print("File does not exist. Creating a new file...")

    #     # Prepare data to create the new file
    #     create_data = {
    #         'message': commit_message,
    #         'content': encoded_content
    #     }

    #     # Make the PUT request to create the file
    #     create_response = requests.put(file_url, headers={'Authorization': f'token {GITHUB_TOKEN}'}, json=create_data)

    #     if create_response.status_code == 201:
    #         print(f"Successfully created the file and triggered the GitHub action.")
    #     else:
    #         print(f"Failed to create the file: {create_response.status_code}, {create_response.text}")

    # else:
    #     print(f"Failed to check file existence: {response.status_code}, {response.text}")
    time.sleep(17)
    return {"answer": "https://hub.docker.com/repository/docker/hardikiitm/your_repo_name/general"}

def qga2_9():
    return {"answer": 'https://ga2-9.vercel.app/api'}

def qga3_1(categories:str, test_case:str):
    result = f'''import httpx

def analyze_sentiment():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {{
        "Authorization": "Bearer dummy_api_key",
        "Content-Type": "application/json"
    }}
    
    data = {{
        "model": "gpt-4o-mini",
        "messages": [
            {{"role": "system", "content": "Analyze the sentiment of the following text and classify it as one of the following: {categories}"}},
            {{"role": "user", "content": {test_case}}}
        ]
    }}
    
    try:
        response = httpx.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        print(result)
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {{e}}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {{e}}")

if __name__ == "__main__":
    analyze_sentiment()'''
    return {"answer": result}

async def qga3_2(message:str):
    result = await process_task(message)
    result = result["usage"]["prompt_tokens"]
    return {"answer": result}

def qga3_3(model: str, system_message: str, user_message: str, fields: str, additional_properties:str):
    print(fields)
    try:
        fields = ast.literal_eval(fields)  # This safely evaluates the string into a list of dictionaries
    except ValueError as e:
        raise ValueError(f"Invalid format for fields: {e}")

    if additional_properties.lower() == "true":
        additional_properties = True
    elif additional_properties.lower() == "false":
        additional_properties = False

    # Validate that fields is a list of dictionaries
    if not isinstance(fields, list) or not all(isinstance(f, dict) and 'field_name' in f and 'type' in f for f in fields):
        raise ValueError("The fields argument must be a list of dictionaries with 'field_name' and 'type'.")

    # Dynamically create the "properties" for the "addresses" based on the fields list
    properties = {}
    required_fields = []

    for field in fields:
        field_name = field['field_name']
        field_type = field['type']

        # Validate the field type
        if field_type not in ["string", "number"]:
            raise ValueError(f"Invalid type for field {field_name}: {field_type}. Must be 'string' or 'number'.")

        # Add to properties and required fields
        properties[field_name] = {
            "type": field_type
        }
        required_fields.append(field_name)

    # Create the JSON body as a dictionary
    json_body = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "address_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "addresses": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": properties,
                                "required": required_fields,
                                "additionalProperties": bool(additional_properties)
                            }
                        }
                    },
                    "required": ["addresses"],
                    "additionalProperties": bool(additional_properties)
                }
            }
        }
    }

    # Return the JSON body as a string
    return json.dumps(json_body, indent=2)

def qga3_4():
    data_dir = "data"
    image_files = [f for f in os.listdir(data_dir) if f.lower().endswith(".png")]

    if len(image_files) == 1:
        input_path = os.path.join(data_dir, image_files[0])  # Get the full path of the image file
    else:
        input_path = "assets/download.png"
    

    # Open the image file in binary mode
    with open(input_path, "rb") as image_file:
        # Read the image data
        image_data = image_file.read()
        
        # Encode the image data to Base64
        base64_encoded = base64.b64encode(image_data).decode("utf-8")
        
        # Get the file extension to set the correct MIME type
        file_extension = input_path.split('.')[-1]
        
        # Create the base64 URL (data URI scheme)
        base64_url = f"data:image/{file_extension};base64,{base64_encoded}"

        return {"answer": base64_url}

def qga3_5(model_name:str, messages:str):
    # Create the JSON structure
    request_data = {
        "model": model_name,
        "input": messages
    }
    
    # Convert the dictionary to a JSON string
    result= json.dumps(request_data)
    return {"answer": result}

def qga3_6(function_name:str):

    result = f'''import numpy as np
from itertools import combinations

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def {function_name}(embeddings):
    max_similarity = -1  # Initialize with a low value
    most_similar_pair = None
    
    for phrase1, phrase2 in combinations(embeddings.keys(), 2):
        similarity = cosine_similarity(np.array(embeddings[phrase1]), np.array(embeddings[phrase2]))
        
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_pair = (phrase1, phrase2)
    
    return most_similar_pair
'''
    result = json.dumps(result)
    return {"answer": result}
    
def qga3_7():
    return {"answer": 'https:localhost:8002/similarity'}

def qga3_8():
    return {"answer": 'https:localhost:8004/execute'}
