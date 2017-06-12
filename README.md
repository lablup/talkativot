Talkativot: Do-It-Yourself backbone for your AI friend
======================================================

Chat-bot barebone for testing the possibility of bot-based service.


![version](https://img.shields.io/badge/version-0.1a-red.svg)

## Status

![miki](https://img.shields.io/badge/codename-miki-red.svg)

## Supported bot services
 * [Telegram](https://telegram.org)

### Required Environment Variables

 * Mandatory
  * `TALKATIVOT_TELEGRAM_TOKEN`: telegram token to attach bot.

 * Optional
   * `TALKATIVOT_DEV_MODE=1`: `true` to enable dev mode
    * 0 (or unset) : production mode
    * 1 : development mode (local django runserver)
    * 2 : development mode (dockerized)

## Bot testing

### Individual testing
After [creating bot account via BotFather](https://telegram.me/BotFather), add shell environments:

 * `export TALKATIVOT_DEV_MODE=1`
 * `export TALKATIVOT_TELEGRAM_TOKEN=[TOKEN YOU GAVE FROM BOTFATHER]`

You *should* use your own bot API token: Token for `ArchaeoBot` is used by testing server and request with same token causes confliction between bot servers.

And you can run your bot via `python3 ./serve/nest.py`.

### Setting up docker development environment

Will soon be prepared. (Still too simple to be dockerized!)

## Structure

Talkativot consists of two main parts: bot server and decision engine.

 * Bot server
   * Interface for bot service APIs.
   * Communicate with decision engine via REST
 * Decision module
   * 'Real' bot engine
   * Consists of
     * Context parser
     * Decision graph
     * Feature modules
