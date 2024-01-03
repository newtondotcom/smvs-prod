const amqp = require('amqplib');

const rabbitMQUrl = 'amqp://141.145.217.120:5672';
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

async function sendTask(task) {
  try {
    if (!connection || !channel) {
      // If the connection or channel is not initialized, initialize them
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

// Initialize the connection and channel before sending the first task
initialize();

  // Example usage: send a task to the worker
var dic = {};
dic["taskData"] = "This is a sample task";
dic["email"] = "test@gmail.com";
dic["silence"] = true;
const task = dic;
sendTask(task);