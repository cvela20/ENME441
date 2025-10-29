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
    <html>
    <head>
    <title>LED Brightness Control</title>
    </head>
    <body>

      <p1>Brightness Level:</p1>
      <form action="/cgi-bin/led_control.py" method="POST">
      <input type="range" name="slider1" min="0" max="100" value="25">

      <p>Select LED:</p>
      <input type="radio" name="option" value="1" checked> LED 1 ({brightness[0]}%)<br>
      <input type="radio" name="option" value="2"> LED 2 ({brightness[1]}%)<br>
      <input type="radio" name="option" value="3"> LED 3 ({brightness[2]}%)<br>

      <input type="submit" value="Change Brightness">
      </form>

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
s.bind(('', 8080))
s.listen(1)

serve_web_page()