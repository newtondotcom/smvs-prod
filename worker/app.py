import pika

print(' Connecting to server ...')

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1",port=5672))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")
    exit()
    
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print(' Waiting for messages...')


def callback(ch, method, properties, body):
    print(" Received %s" % body.decode())

    ## Parameters
    file_s3_id = "server1"
    file_s3_name = "file1"
    emoji = True

    #Download file from S3

    #Process file

    #Upload file to S3


    #Advice server that file is ready

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()