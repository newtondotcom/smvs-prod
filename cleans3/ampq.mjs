import amqp from 'amqplib';

const rabbitMQUrl = 'amqp://144.91.123.186:15672';
const exchange = 'tasks';
const workerQueue = 'task_queue';

let connection, channel;

async function initialize() {
    try {
      connection = await amqp.connect(rabbitMQUrl);
      channel = await connection.createChannel();
  
      // Declare the exchange and queue
      await channel.assertExchange(exchange, 'direct', { durable: false });
      await channel.assertQueue(workerQueue, { durable: true });
      await channel.bindQueue(workerQueue, exchange, '');
  
      console.log('Initialized connection and channel.');
  
    } catch (error) {
      console.error(`Error initializing connection and channel: ${error.message}`);
    }
  }

initialize()


export async function sendTask(task) {
    try {
      if (!connection || !channel) {
        await initialize();
      }
  
      // Send the task as a JSON string
      const taskJSON = JSON.stringify(task);
      channel.sendToQueue(workerQueue, Buffer.from(taskJSON));
  
      console.log(`Sent task: ${taskJSON}`);
    } catch (error) {
      console.error(`Error sending task: ${error.message}`);
    }
  }