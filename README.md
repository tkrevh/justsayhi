# JustSayHi Slack APP

I'm following Sam Parr on Twitter and he posted this:

![Sam Parr Tweet](https://i.ibb.co/rsWtnZB/2022-11-08-01-46-17-Sam-Parr-on-Twitter-Tinkering-with-Slack-as-a-community-platform-One-thing-I.png)

He was right, Slack bot can not what he wants.  
So I've built this Slack app for him in one afternoon.  
See it live at [justsayhi.xyz](https://justsayhi.xyz)

## What is it?
It is a simple Django app with a Slack OAuth integration.  
It automatically sends a configurable message to a newly joined person in the Slack workspace.

## How to run

You will need a `.env` file with the following variables:
```
DATABASE_URL=
DEBUG=
SECRET_KEY=
SLACK_CLIENT_ID=
SLACK_CLIENT_SECRET=
```

Then run
`docker-compose up`
