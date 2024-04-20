const buckets = [
    {
        name : "videos",
        endpoint : process.env.S3_HOST,
        port : process.env.S3_PORT,
        accessKey : process.env.S3_KEY_ID,
        secretKey : process.env.S3_SECRET_KEY,
    }
]

export default buckets;