#Cameron Vela Lab 8 Question 1

import socket
from RPi import GPIO

#Set up output pins and pwm signals going to output pins
GPIO.setmode(GPIO.BCM)
pins = [17,27,22]

for p in pins:
    GPIO.setup(p, GPIO.OUT)

f = 500

pwms = [GPIO.PWM(p, 500) for p in pins]

for pwm in pwms:
    pwm.start(0)
brightness = [0, 0, 0]

# Parse function from class
def parsePOSTdata(data):
    data_dict = {}
    idx = data.find('\r\n\r\n')+4
    data = data[idx:]
    data_pairs = data.split('&')
    for pair in data_pairs:
        key_val = pair.split('=')
        if len(key_val) == 2:
            data_dict[key_val[0]] = key_val[1]
    return data_dict

def web_page():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>LED Brightness Control</title>
    </head>
    <body>
      <h2>LED Brightness Control</h2>

      <p>Move any slider to change LED brightness:</p>

      <p>
        LED 1: <input id="s1" type="range" min="0" max="100" value="{brightness[0]}">
        <span id="v1">{brightness[0]}</span>%
      </p>

      <p>
        LED 2: <input id="s2" type="range" min="0" max="100" value="{brightness[1]}">
        <span id="v2">{brightness[1]}</span>%
      </p>

      <p>
        LED 3: <input id="s3" type="range" min="0" max="100" value="{brightness[2]}">
        <span id="v3">{brightness[2]}</span>%
      </p>

      <script>
        function sendUpdate(led, value) {{
          fetch("/", {{
            method: "POST",
            headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
            body: "slider1=" + value + "&option=" + led
          }});
        }}

        // Handle LED 1
        const s1 = document.getElementById("s1");
        s1.oninput = () => {{
          document.getElementById("v1").textContent = s1.value;
          sendUpdate(1, s1.value);
        }};

        // Handle LED 2
        const s2 = document.getElementById("s2");
        s2.oninput = () => {{
          document.getElementById("v2").textContent = s2.value;
          sendUpdate(2, s2.value);
        }};

        // Handle LED 3
        const s3 = document.getElementById("s3");
        s3.oninput = () => {{
          document.getElementById("v3").textContent = s3.value;
          sendUpdate(3, s3.value);
        }};
      </script>
    </body>
    </html>
    """
    return html.encode('utf-8')


def serve_web_page():
    while True:
        print('Waiting for connection...')
        conn, (client_ip, client_port) = s.accept() 
        print(f'Connection from {client_ip} on client port {client_port}')
        client_message = conn.recv(2048).decode('utf-8')
        print(f'Message from client:\n{client_message}')
        data_dict = parsePOSTdata(client_message)

        if 'slider1' in data_dict.keys() and 'option' in data_dict.keys():   # make sure data was posted
            led_brightness = int(data_dict["slider1"])
            led_number = int(data_dict["option"])
            if led_number == 1:
                brightness[0] = led_brightness
                pwms[0].ChangeDutyCycle(brightness[0])
            elif led_number == 2:
                brightness[1] = led_brightness
                pwms[1].ChangeDutyCycle(brightness[1])
            elif led_number == 3:
                brightness[2] = led_brightness
                pwms[2].ChangeDutyCycle(brightness[2])

        conn.send(b'HTTP/1.1 200 OK\r\n')                  # status line
        conn.send(b'Content-Type: text/html\r\n')          # headers
        conn.send(b'Connection: close\r\n\r\n')   
        conn.sendall(web_page())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(1)

serve_web_page()