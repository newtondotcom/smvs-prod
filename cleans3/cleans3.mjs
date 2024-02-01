import {Client} from 'minio';

var minioClient 

const dayBeforeDelete = 5;

export async function cleanS3(bucket) {
    console.log('Cleaning bucket: ' + bucket.name)
    minioClient = new Client({
        endPoint: bucket.endpoint,
        port: bucket.port,
        useSSL: false,
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
    console.log('Done')
    } catch (err) {
        console.log(err)
    }
}