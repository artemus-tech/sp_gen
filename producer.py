import pika

def send_message():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue (it will be created if it doesn't exist)
    channel.queue_declare(queue='task_queue')

    # Send a message to the queue
    message = "Hello from Python!"
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message)
    print(f"Sent: {message}")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    send_message()
