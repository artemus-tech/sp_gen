import pika
import subprocess

# Define functions to run different scripts
def run_script_1():
    print("Running Script 1...")
    subprocess.run(["python", "sp_df.py"])

def run_script_2():
    print("Running Script 2...")
    subprocess.run(["python", "script2.py"])

def handle_message(message):
    # Depending on the message, run different scripts
    if message == "run_script_1":
        run_script_1()
    elif message == "run_script_2":
        run_script_2()
    else:
        print(f"Unknown message: {message}")

# Establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='python_script_queue')

# Define the callback function to process received messages
def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Received {message}")
    handle_message(message)

# Set up the consumer to listen for messages
channel.basic_consume(queue='python_script_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
