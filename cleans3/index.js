var Minio = require('minio')

/*
export default function generateUniqueName() {
    let date = new Date();
    let timestamp = date.getTime();
    let randomString = Math.random().toString(36).substring(2, 8); 
    let uniqueName = `${timestamp}_${randomString}`;
    return uniqueName;
}
*/

var minioClient 

const buckets = [
    {
        name : 'bucket1',
        endpoint : 'play.min.io',
        port : 9000,
        accessKey : 'Q3AM3UQ867SPQQA43P2F',
        secretKey : 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'
    },
    {
        name : 'bucket1',
        endpoint : 'play.min.io',
        port : 9000,
        accessKey : 'Q3AM3UQ867SPQQA43P2F',
        secretKey : 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'   
    }
]

const dayBeforeDelete = 5;

async function cleanS3(bucket) {

    minioClient = new Minio.Client({
        endPoint: bucket.endpoint,
        port: bucket.port,
        useSSL: true,
        accessKey: bucket.accessKey,
        secretKey: bucket.secretKey,
    })

  try {
    const list = await minioClient.listObjects(bucket.name, '', true)
    const objects = list.map((obj) => obj.name)
    objects.forEach((obj) => {
        const date = obj.split('_')[0]
        const objDate = new Date(date)
        const today = new Date()
        const diff = today - objDate
        const days = diff / (1000 * 60 * 60 * 24)
        if (days > dayBeforeDelete) {
            minioClient.removeObject(bucketName, obj, function(err) {
                if (err) {
                    return console.log(err)
                }
            })
        }
  } )
    } catch (err) {
        console.log(err)
    }
}

var cron = require('node-cron');

cron.schedule('0 3 * * *', () => {
    console.log('Running a task every day at 3am');
    buckets.forEach((bucket) => cleanS3(bucket))
  });