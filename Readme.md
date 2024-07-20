# What

A simple project that integrates an llm into a Telegram bot using Python and Ollama. The bot is intended to be used in group chats.

Also an experiment with devcontainers

# Usage guide

## Prerequisites

To use this project, you will need:

* Git
* Docker

## How to run your own instance

1. Clone the repository

```git clone https://github.com/Jarki/telellama```

2. Rename the ```.env.example``` file into ```.env```

3. Edit the content of the renamed file to add the following variables:

```TELEGRAM_TOKEN``` Use the token you received from BotFather. [Obtain your bot token.](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)

```MODEL_NAME``` (Optional) Choose any model from https://ollama.com/library. If not provided, will use llama3

```OLLAMA_HOST``` (Optional) **Only change this if you know what you're doing** Address of ollama API. Default http://ollama:11434, which exists inside the docker network

4. Run ```docker-compose up```. Now, the bot works!

## Bot documentation

The Telegram bot itself will:

* Reply to any message which is a reply to the bot.

* Respond to /ping commands with a Pong message. Use it to quickly get a message from the bot to reply to.

# Development guide

Telellama was developed using devcontainers. To learn about devcontainers, follow [this](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers) guide.

## General

Devcontainer config looks at ```docker-compose.debug.yml```. Local workspace is mounted into the /app directory of telellama container.

## VSCode extensions used inside of the container

[ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) - Python intellisense + needed for other extensionss

[ms-python.debugpy](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy) - Useful tool for debugging Python

[ms-vscode-remote.remote-containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) - Not sure what it does. Looks like maybe needed for devcontainers?

[ms-azuretools.vscode-docke](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) - Not sure why. Probably need to remove it

## Features used

[ghcr.io/devcontainers-contrib/features/curl-apt-get:1](https://github.com/devcontainers-contrib/features/tree/main/src/curl-apt-get) - Useful for debugging networking

[ghcr.io/devcontainers/features/git:1](https://github.com/devcontainers/features/tree/main/src/git) - Adds git into the devcontainer 