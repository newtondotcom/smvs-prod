# Yogocap - BackEnd 🎥

This repo contains everything needed for the Yogocap Backend. 

Right below, you can read how the repo structure is built:

### Worker 🛠️

This is where the main magic happens. It combines [whisperX](https://github.com/m-bain/whisperX) and [FFmpeg](https://github.com/FFmpeg/FFmpeg) to generate social media video subtitles with word-level timestamps and coloration. The worker listens for incoming tasks on [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server) sent by the [NuxtJs](https://github.com/nuxt/nuxt) [Yogocap's FrontEnd](https://github.com/newtondotcom/yogocap-nuxt).

### FakeRabbitMQ 🐇

This folder contains two servers: [one in Python](https://github.com/python/cpython) and [one based on Node.js](https://github.com/nodejs/node), that emulate [Yogocap's FrontEnd](https://github.com/newtondotcom/yogocap-nuxt) by sending tasks to [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server)'s queue on execution.

### Inputs 🎬

This folder contains test videos for the worker and for the two servers.

### Server ⏰

This acts as a cron job to clean the S3 bucket of videos not used for 5 days.

> Deprecated: [Minio](https://github.com/minio/minio) provides Lifecycle Rules for this purpose.

## License 📜

This software is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License [CC BY-NC 4.0]. For details, see [LICENSE](LICENSE).