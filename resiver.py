import asyncio
import websockets

async def handle_message(websocket, path):
    async for message in websocket:
        # Process the received message from the Streamlit web page
        print('Received:', message)

        # Perform corresponding actions based on the message content
        if message == 'ReloadTable':
            # Perform table reload operation
            print('Table reload triggered')
            # ...

async def main():
    server = await websockets.serve(handle_message, 'localhost', 8501)

    print('WebSocket server started')

    try:
        await server.wait_closed()
    except KeyboardInterrupt:
        pass

    print('WebSocket server stopped')

if __name__ == '__main__':
    asyncio.run(main())
