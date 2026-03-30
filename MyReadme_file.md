## First thing you have to change the directory to the project folder
-> cd youtube_audio_web
-> cd app
-> uvicorn main:app --reload

### first we have to create the virtual environment ###

-> python -m venv venv

### activate the virtual environment ###

-> venv\Scripts\activate  (for Windows)

### Install the required packages ###
-> pip install -r requirements.txt

### To run the server ###
python -m uvicorn app.main:app --reload

    -> main.app means "main.py file is located in app folder so that's why we are using main.app", if it is in root directory then just use main ex: "python -m uvicorn main:app --reload" "

    -> To run the server: uvicorn app.main:app --reload





### test_deepfilter.py ###
-> used this file to test the deepfilter model separately before integrating into the web app.
-> Mainly it is used for testing purpose whether the audio is cleaned or not(means audio background noise removed or not).









### Workflow steps
-> Create logic file(.py file), .html file
-> import logic to the main file
-> add get method route and api route(post method) to the main function
-> add the dictionary to the history("type_converter":[])
-> add the onclick button to the layout file
->add dictionary to the history.json file (Eg: ADD THIS "type_converter:[]")