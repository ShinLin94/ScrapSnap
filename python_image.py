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
