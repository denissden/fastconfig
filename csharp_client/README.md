# FastConfig client for C#

Get configuration for your c# applications easily.

- [FastConfig client for C#](#fastconfig-client-for-c)
  - [Connect to FastConfig server](#connect-to-fastconfig-server)
      - [Using environment variables](#using-environment-variables)
  - [Get configuration](#get-configuration)
  - [Send configuration](#send-configuration)
  - [Dependency Injection](#dependency-injection)

## Connect to FastConfig server
To connect to FastConfig you need
- `Address`
- `AppId` - unique application name
- `Token` - token created for a specific AppId or a master token
  
```csharp
var fastConfig = new FastConfigClient(
  address: address,
  appId: appId,
  token: token
);
```

#### Using environment variables
Connection configuration is stored in following environment variables:
- `FASTCONFIG_ADDRESS`
- `FASTCONFIG_APPID`
- `FASTCONFIG_TOKEN`

By passing a parameter you can override the env variable. In this case `Address` and `Token` are storen in environment variables and `AppId` is stored in code.
```csharp
var fastConfig = FastConfigClient.FromEnvironment(
  appId: appId, 
);
```

## Get configuration

Get configuration deserialized into your type.
```csharp
var appConfig = await fastConfig.Get<YourConfig>();
```

Get configuration as a string.
```csharp
string appConfig = await fastConfig.Get();
```

## Send configuration

Send a class instance.
```csharp
var config = new AnyClass();
await fastConfig.Send(config);
```

Send a string. The string must be a valid json.
```csharp
await fastConfig.Send("{\"foo\": \"bar\"}");
```

## Dependency Injection
You can add a FastConfig client to services using `AddFastConfig`.
```csharp
var fastConfig = FastConfigClient.FromEnvironment();
...
services.AddFastConfig(fastConfig);
```