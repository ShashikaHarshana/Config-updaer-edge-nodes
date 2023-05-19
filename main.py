# This is the config updater which runs in the edge nodes.
from urllib import request

import requests
from flask import Flask

app = Flask(__name__)

class ConfigUpdater(object):

    def __init__(self):
        self.esp32_url = 'http://192.168.47.235/'
        self.config_updater_url = 'http://localhost:3000'

    def get_curr_frame_size(self):
        config_url = self.esp32_url + 'config'

        response = requests.get(config_url)

        if response.status_code == 200:
            curr_frame_size = response.text

        else:
            print('Request failed with status code:', response.status_code)

        return curr_frame_size

    def get_frame_size(self, frame_size, target):
        frame_sizes = ['5', '8', '9', '13']  # Example frame sizes, modify as needed

        index = frame_sizes.index(frame_size)

        if target == 'high':
            if index == len(frame_sizes) - 1:
                return frame_sizes[index]  # Return the highest frame size
            else:
                return frame_sizes[index + 1]  # Return the higher frame size
        elif target == 'low':
            if index == 0:
                return frame_sizes[index]  # Return the lowest frame size
            else:
                return frame_sizes[index - 1]  # Return the lower frame size
        elif target == 'highest':
            return frame_sizes[len(frame_sizes) - 1]

        elif target == 'minimum':
            return frame_sizes[0]

        else:
            return None  # Invalid target argument

    def get_request_payload(self, quality_measure):
        curr_size = self.get_curr_frame_size()

        if quality_measure == 'increase':
            req_frame_size = self.get_frame_size(curr_size, 'high')
            return req_frame_size

        else:
            req_frame_size = self.get_frame_size(curr_size, 'low')
            return req_frame_size

    def print_hi(self, name):
        # Define the ESP32 web server URL

        # Define the event or condition that triggers the HTTP request
        event_occurred = True

        if event_occurred:
            # Create a payload if required
            payload = {'key1': 'value1', 'key2': 'value2'}

            # Send an HTTP GET or POST request to the ESP32 web server
            response = requests.post(self.esp32_url, data=payload)

            # Check the response status code
            if response.status_code == 200:
                print('HTTP request sent successfully')
            else:
                print('Failed to send HTTP request')

    def update_config(self, update_req):
        req_url = self.esp32_url + 'control'
        get_req_framesize = self.get_request_payload(update_req)
        params = {'quality': get_req_framesize}

        response = requests.get(req_url, params=params)

        if response.status_code == 200:
            print(response.text)
        else:
            print('config update failed with status code: ', response.status_code)

    def main(self):

        # Start Flask server
        app.run(host='0.0.0.0', port=5000)
        print("flask server started.....")

        @app.route("/", methods=['GET'])
        def hello_from_updater():
            return "hello world"

        @app.route('/update-config', methods=['GET'])
        def update_config():
            update_req = request.args.get('update_req')
            ConfigUpdater_ob.update_config(update_req)

if __name__ == '__main__':
    ConfigUpdater_ob = ConfigUpdater()
    ConfigUpdater_ob.main()
