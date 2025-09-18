# app/main.py
import asyncio
import base64
import json
import cv2
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.mediapipe_runner import MediaPipeRunner
import pyautogui

app = FastAPI()
runner = MediaPipeRunner(0)

clients = set()

# Track mouse mode per client
mouse_enabled = {}

async def camera_loop():
    while True:
        result = runner.process()
        if result is None:
            await asyncio.sleep(0.01)
            continue

        frame, meta = result

        if meta:
            x, y = meta.get("x"), meta.get("y")
            gesture = meta.get("gesture")

            if x is not None and y is not None:
                screen_w, screen_h = pyautogui.size()
                px, py = int(x * screen_w), int(y * screen_h)

                
                for ws, enabled in mouse_enabled.items():
                    if enabled:
                        if gesture == "point":
                            pyautogui.moveTo(px, py)

                        elif gesture == "pinch":
                            
                            if py < screen_h // 2:
                                pyautogui.scroll(5)
                            else:
                                pyautogui.scroll(-5)

                        elif gesture == "open":
                            
                            pyautogui.click(px, py)

        
        _, jpg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        jpg_bytes = jpg.tobytes()
        b64 = base64.b64encode(jpg_bytes).decode("ascii")

        message = {"type": "frame", "jpeg_base64": b64, "meta": meta}

        websockets = list(clients)
        for ws in websockets:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                clients.discard(ws)
                mouse_enabled.pop(ws, None)

        await asyncio.sleep(0.02)  


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(camera_loop())


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    mouse_enabled[ws] = False

    try:
        while True:
            data = await ws.receive_text()
            try:
                cmd = json.loads(data)
                if cmd.get("action") == "mouse_enable":
                    mouse_enabled[ws] = True
                elif cmd.get("action") == "mouse_disable":
                    mouse_enabled[ws] = False
            except:
                pass
    except WebSocketDisconnect:
        clients.discard(ws)
        mouse_enabled.pop(ws, None)


@app.get("/")
async def root():
    return {"status": "Backend running with MediaPipe/MoveNet"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
