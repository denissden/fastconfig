string token = "7bd93468-3b23-4aa1-b088-d68f945f299c"; // insert token here
if (string.IsNullOrEmpty(token))
{
    throw new ArgumentException("Please insert a token");
}
string address = "http://localhost:5000/";
string appId = "chat";

var client = new FastConfig.FastConfigClient(address, appId, token);

// create and send config
var config = new Example.Config();
config.ServiceId = 1337;
config.Connections.Database = "server=postgre;password=password";
config.Connections.RabbitMQ = "server=localhost:5672;password=password";
config.Urls.Api = "https://someapi.com/";
config.Urls.Auth = "https://auth.someserver.com/";
await client.SendConfig(config);
Console.WriteLine("Config sent");

// get config
Console.WriteLine("Getting config");
var received = await client.GetConfig<Example.Config>();
Console.WriteLine("-----Config-----");
Console.WriteLine(received);
Console.WriteLine("----------------");
Console.WriteLine("Success");






