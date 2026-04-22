import time
import serial

def capture_image():
    ser = serial.Serial('COM5', 115200, timeout=1)

    time.sleep(2)
    ser.reset_input_buffer()
    ser.write(b'c')

    start_time = time.time()
    buffer = bytearray()

    # --- collect all incoming data ---
    while True:
        if time.time() - start_time > 20:
            raise Exception("Timeout during capture")

        chunk = ser.read(1024)
        buffer.extend(chunk)

        # stop once we see CAPTURE_END
        if b"CAPTURE_END" in buffer:
            break

    ser.close()

    # --- extract JPEG ---
    start = buffer.find(b'\xff\xd8')  # JPEG start
    end = buffer.find(b'\xff\xd9')    # JPEG end

    if start == -1 or end == -1:
        raise Exception("JPEG markers not found")

    jpg_data = buffer[start:end+2]

    with open("image.jpg", "wb") as f:
        f.write(jpg_data)

    return "image.jpg"











# import time

# import serial
# # import os
# # from estimate_calories import estimate_calories

# def capture_image():
#     ser = serial.Serial('COM5', 115200, timeout=1)
#     time.sleep(2)                 # wait for Arduino reset
#     ser.reset_input_buffer()      # clear junk
#     ser.write(b'c')               # send command

#     start_time = time.time()
#     img_data = bytearray()

#     buffer = b""
    
#     started = False

#     while True:
#         if time.time() - start_time > 10:  # 10 sec timeout
#             raise Exception("Timeout waiting for image")

#         buffer += ser.read(64)

#         if b"CAPTURE_START" in buffer:
#             break

#     while True:
#         if time.time() - start_time > 15:
#             raise Exception("Timeout during image transfer")

#         chunk = ser.read(1024)

#         if b"CAPTURE_END" in chunk:
#             chunk = chunk.split(b"CAPTURE_END")[0]
#             img_data.extend(chunk)
#             break

#         img_data.extend(chunk)

#     with open("image.jpg", "wb") as f:
#         f.write(img_data)

#     ser.close()
#     return "image.jpg"






#     data = bytearray()
#     recording = False

#     while True:
#         chunk = ser.read(1024)

#         if b"CAPTURE_START" in chunk:
#             data = bytearray()
#             recording = True
#             continue

#         if b"CAPTURE_END" in chunk:
#             break

#         if recording:
#             data.extend(chunk)

#     filename = "image.jpg"
#     with open(filename, "wb") as f:
#         f.write(data)

#     return filename

# # # 🚀 TRIGGER CALORIE ESTIMATION HERE
# # estimate_calories(filename)