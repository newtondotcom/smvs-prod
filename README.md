# Yogocap - BackEnd

This repo contains everything needed for the Yogocap Backend. 

Righ after, I have explained each directory role.

## Server

This acts as a cron job to clean S3 bucket with videos not used for 5 days. 

## Worker

This is where the main magic is happening. Its combines (whisperX)[https://github.com/m-bain/whisperX] and (ffmpeg)[https://github.com/FFmpeg/FFmpeg] uses to generate social media videos subtitles with word level timestamp and coloration. The worker listens for incoming task on (RabbitMQ)[https://github.com/rabbitmq/rabbitmq-server] sent by the (NuxtJs)[https://github.com/nuxt/nuxt] (Yogocap's FrontEnd)[https://github.com/newtondotcom/yogocap-nuxt].

## FakeRabbitMQ

This folder contains two servers (one in (Python)[https://github.com/python/cpython] and one based on (NodeJ)[https://github.com/nodejs/node]) that emulates the (Yogocap's FrontEnd)[https://github.com/newtondotcom/yogocap-nuxt] by sending task on (RabbitMQ)[https://github.com/rabbitmq/rabbitmq-server]'s queue on execution.

## Inputs

This folder contains test videos for the worker and for the two servers.

> License :

This software is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). For details, see (LICENSE)[LICENSE]
