// CLEAN S3
import { cleanS3 } from './cleans3.mjs'; // Update the file extension
import cron from 'node-cron';
import buckets from './buckets.mjs'; // Update the file extension

cron.schedule('0 3 * * *', () => {
  console.log('Running a task every day at 3am');
  buckets.forEach((bucket) => cleanS3(bucket));
});

// REDIRECT AMPQ
import express from 'express';
import bodyParser from 'body-parser';
import * as ampq from './ampq.mjs'; // Update the file extension
import cors from 'cors';
const app = express();

app.use(bodyParser.json());
app.use(cors());

app.listen(3000, () =>
  console.log('Example app listening on port 3000!')
);

app.post('/', (req, res) => {
    let body = req.body;
    console.log('Received body:', body);
    ampq.sendTask(body);
    res.status(200).send('Task sent to AMPQ');
  });
