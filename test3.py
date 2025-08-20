import websocket
import json
import threading

# Bybit WebSocket URL for the public market data
ws_url = "wss://stream.bybit.com/v5/public/spot"


def on_message(ws, message):
    data = json.loads(message)
    print("Received message:", json.dumps(data, indent=4))


def on_error(ws, error):
    print("Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")


def on_open(ws):
    # Subscribe to the order book for a specific symbol
    subscribe_message = {
        "op": "subscribe",
        "args": [
            "orderbook.50.BTCUSDT"
        ],
        "req_id": "test"

    }
    ws.send(json.dumps(subscribe_message))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Run the WebSocket in a separate thread
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    # Keep the main thread alive
    while True:
        pass
