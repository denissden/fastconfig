# FastConfig
Store configurations for multiple applications in one place

- [FastConfig](#fastconfig)
  - [Quick start](#quick-start)
        - [1. install dependencies](#1-install-dependencies)
        - [2. start the server](#2-start-the-server)
        - [3. create a token for an app](#3-create-a-token-for-an-app)
        - [4. send configuration](#4-send-configuration)
        - [5. get configuration](#5-get-configuration)
  - [Server configuration](#server-configuration)
  - [API](#api)
      - [Tokens](#tokens)
      - [Requests](#requests)
  - [Clients](#clients)

## Quick start

##### 1. install dependencies
`pip install -r requirements.txt`

##### 2. start the server
Run `serve.py --environment prod`.
On the first run a *master token* will be printed. 
If you lost the master token you can find it in [storage/__tokens.json](server/storage/__tokens.json) (link only works locally)

##### 3. create a token for an app
You can use any http client like [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) to work with API

Get a token for an `exampleApp` app
```http
GET http://localhost:5000/token/exampleApp/new
token: insert master token here
```

##### 4. send configuration
Use a token you received in the last step
```http
PUT http://localhost:5000/configuration/chat
token: insert exampleApp token here

{ "foo": "bar" }
```

##### 5. get configuration

Get `exampleApp` config using an HTTP request
```http
GET http://localhost:5000/configuration/exampleApp
token: insert exampleApp token here
```

## Server configuration
By default FastConfig is serving on `localhost:5000`
You can configure FastConfig server using the following environment variables:
- `HOST` - serve host (ex. `127.0.0.1`)
- `PORT` - serve port (ex. `6000`)

## API
#### Tokens
To work with API you have to add a `token` header containing your token.

Token access levels:
- `master token`
  - create and update app tokens
  - get and update any configuration
- `app token` 
  - get and update only its app configuration


#### Requests
Variable values are marked with `*...*` (ex. `*appId*`)

`/token/*appId*/new` 
- first request creates a token, next ones update the token
  
`/configuration/*appId*` 
- **GET** - get stored config
- **PUT** - send a new config, delete previous one

`/configuration`
- **GET** - get configs for all apps as a single json

## Clients
- `C#` - [dotnet client](csharp_client)

Support for other languages coming soon. 