import pika
import subprocess

# Define functions to run different scripts
def run_script_1():
    print("SP_DF_VOLUME_FRACTION")
    subprocess.run(["python", "sp_df_vf.py"])

def run_script_2():
    print("SP_INTENSITY_EVALUATION")
    subprocess.run(["python", "sp_weave_eval_process_optimize.py"])

def handle_message(message):
    # Depending on the message, run different scripts
    if message == "sp_df_vf":
        run_script_1()
    elif message == "sp_eval":
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
