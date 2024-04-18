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
import cors from 'cors';
const app = express();

app.use(bodyParser.json());
app.use(cors());

app.listen(3000, () =>
  console.log('Example app listening on port 3000!')
);
