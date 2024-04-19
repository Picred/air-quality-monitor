import asyncio
import time, socket

def testLogstash():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('logstash', 5000))
            sock.close()
            print("[ingestion-manager]Logstash is ready!")

            break
        except:
            print("[ingestion-manager]Logstash not ready")
            time.sleep(5)
            continue


def main() -> None:
    testLogstash()
    


if __name__ == '__main__':
    try:
        asyncio.run(main())     
    except KeyboardInterrupt:
        print("[ingestion-manager]Program exited")
