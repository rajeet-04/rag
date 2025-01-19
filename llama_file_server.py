import requests
import base64



def send_image_get_stream(image_path, input):
    # Encode the image to base64
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    _prompt = """A chat between a curious human and an artificial intelligence assistant.
    The assistant gives helpful, detailed, and polite answers to the human's questions
    USER:[img-10]{prompt}
    ASSISTANT:""".format(prompt=input)

    # Prepare the JSON body for the request
    json_body = {
        # "stream": True,
        "stream" : False,
        "n_predict": 350,
        "temperature": 0.8,
        "stop": ["</s>", "Llama:", "User:"],
        "repeat_last_n": 78,
        "repeat_penalty": 1.18,
        "top_k": 40,
        "top_p": 1,
        "min_p": 0.05,
        "tfs_z": 1,
        "typical_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "mirostat": 2,
        "mirostat_tau": 5,
        "mirostat_eta": 0.1,
        "grammar": "",
        "n_probs": 0,
        "min_keep": 0,
        "image_data": [{"data": base64_image, "id": 10}],
        "cache_prompt": True,
        "api_key": "",
        "slot_id": 0,
        "prompt": _prompt
    }

    # Headers as before...
    headers = {
        # "accept": "text/event-stream",
        "accept-language": "en-US,en",
        "cache-control": "no-cache",
        "content-type": "application/json"
    }

    # Send request with stream=True to keep the connection open for streaming
    response = requests.post("http://127.0.0.1:8080/completion", json=json_body,    headers=headers, stream=False)

    return response

'''_input = "Describe this image in details"
response = send_image_get_stream(path, input=_input)
_content = response.json()['content']
print(_content)
_input = """{_content}\n\nMake a list of the three top parts of this image listed as Labels, and their cooresponding coordinates.  Let's think this step by step ...""".format(_content=_content)
'''
while True:
    path=input('Enter image path: ')
    inp=input('Enter prompt: ')
    print(f"Sending {inp}")
    if inp == "exit":
        break
    response = send_image_get_stream(path, input=inp)

    print(response.json()['content'])