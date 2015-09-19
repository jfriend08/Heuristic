# Mint Problem
 Implemented by c++

# Usage
```
g++ -std=c++11 ./exact.cpp
```
```
./a.out 1
```
- Start the server with `npm start` in development mode, `npm run prod` in production mode.
- To setup the development environment
 - Install node (preferably with nvm)
 - Install node dependency with `npm install`
 - (Optional) Install [livereload chrome extension](https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei?hl=en)
- Automatic refresh script
 - Start dev server and livereload with `npm start` and connect your opened page with livereload.
- Test with jest
 - Start jest auto repload test script with `npm test`
 - Get the coverage result with `npm run coverage`

## Firebase setting
When development locally, please apply a firebase database yourself and modify the `development.json` to apply the change. Use import/export data to copy the dev database over for your usage.

# Deploy
**Different version of dockerfile lives inside `/config`**

0. Copy dockerfile from config folder and rename it to `Dockerfile`.
1. Use `docker build -t <dockerusername>/<tagname> .` to build the image.
2. Use `docker run -d -P <dockerusername>/<tagname>` to start the server in the container.
Note: To stop the docker container, use `docker stop $(docker ps -q)` and `docker rm $(docker ps -a -q)`.

## AWS Deploy

0. Run `npm run deploy-dev` to build development zip file and `npm run deploy-prod` to build production zip file.
1. Upload zip file to AWS Elastic Beanstalk environment. Log in to Orderhood AWS console from [here](https://315949786139.signin.aws.amazon.com/console)

## AWS Deploy for Prod environment

After RA 0.1 deployment, runner app has started using `https://web.orderhood.net` as webhood address. And this address is bound to our prod elastic beanstalk through our load balancer setting. As a result of that, getting a environment up and swap the url is no longer sufficient. From now on, when trying to deploy a new version, please follow the following steps.

0. Try deploy to the current app, if success, verify if both `https://web.orderhood.net` and `http://oh-webhood.elasticbeanstalk.com` has been updated.
1. If failed (this happens sometime for no obvious reason), clone the current app and deploy the new binary there.
 0. go to AWS Route 53,  found orderhood.net hosted zone, find the `web.orderhood.net` record set and change the alias target to the new environment’s load balancer
 1. swap the url between two environment
 2. verify the new version is running on `https://web.orderhood.net`
 3. Terminate the old environment and verify  `http://oh-webhood.elasticbeanstalk.com` is having the new environment
