import requests

def test_initialize():
    url = 'http://127.0.0.1:5000/predict_move'
    data = {"filename": "/host_files/board1.txt"}
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Attempt to print the JSON response
        try:
            print(response.json())
        except ValueError as e:
            print("Response is not valid JSON")
            print("Response content:", response.text)

    except requests.exceptions.RequestException as e:
        print("There was an error in making the request:", e)

if __name__ == "__main__":
    test_initialize() 