import cv2
import os
import schedule
import time
from datetime import datetime
from telegram import Bot

# Define the Telegram bot token and chat ID
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'
bot = Bot(token=bot_token)

def capture_image():
    # Capture image from webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        # Save the captured image locally
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        local_image_path = os.path.join('pictures', f'webcam_{timestamp}.jpg')
        cv2.imwrite(local_image_path, frame)

        # Send the image to Telegram
        try:
            with open(local_image_path, 'rb') as f:
                bot.send_photo(chat_id=chat_id, photo=f)
            print(f'Successfully sent {local_image_path} to Telegram')
        except Exception as e:
            print(f'Failed to send {local_image_path} to Telegram: {e}')
    else:
        print('Failed to capture image from webcam')
    cap.release()

# Ensure the local pictures directory exists
os.makedirs('pictures', exist_ok=True)

# Schedule the image capture every 30 minutes
schedule.every(1).minutes.do(capture_image)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
