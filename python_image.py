import serial
# import os
# from estimate_calories import estimate_calories

def capture_image():
    ser = serial.Serial('COM3', 115200, timeout=5)
    ser.write(b'snap\n')

    data = bytearray()
    recording = False

    while True:
        chunk = ser.read(1024)

        if b"CAPTURE_START" in chunk:
            data = bytearray()
            recording = True
            continue

        if b"CAPTURE_END" in chunk:
            break

        if recording:
            data.extend(chunk)

    filename = "image.jpg"
    with open(filename, "wb") as f:
        f.write(data)

    return filename

# # 🚀 TRIGGER CALORIE ESTIMATION HERE
# estimate_calories(filename)