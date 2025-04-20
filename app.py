import cv2
import streamlit as st
import mediapipe as mp
import time

st.title("🤖 Gesture Based Health Monitoring System")
st.markdown("**Show your fingers to control appliances!**")

FRAME_WINDOW = st.image([])

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # index to pinky
    thumb_tip = 4
    count = 0

    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        count += 1

    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1

    return count

prev_count = -1
last_action = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.write("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            fingers = count_fingers(handLms)

            if fingers != prev_count:
                prev_count = fingers
                if fingers == 1:
                    last_action = "🌀 Fan Turned ON"
                elif fingers == 2:
                    last_action = "💡 Light Turned ON"
                elif fingers == 3:
                    last_action = "🌀 Fan Turned OFF"
                elif fingers == 4:
                    last_action = "💡 Light Turned OFF"
                elif fingers == 5:
                    last_action = "🍱 Requesting Food"
                else:
                    last_action = "✋ Idle"

    if last_action:
        cv2.putText(frame, last_action, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
