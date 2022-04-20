using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using FastConfig;


// insert      ||
// token       ||
// here       \\//
//             \/
string token = "";
if (string.IsNullOrEmpty(token))
  throw new ArgumentException("Please insert a token");
string address = "http://localhost:5000/";
string appId = "chat";

var fastConfig = FastConfigClient.FromEnvironment(
  address: address,
  appId: appId,
  token: token
);

if (Example.Ask.YesNo("Do you want to create an example config?"))
{
  var config = Example.CreateConfig.Create();
  await fastConfig.Send(config);
  Console.WriteLine("Config sent");
}

// you may want to get the configuration before configuring the host
Console.WriteLine("Getting config before building the host...");
var appConfig = await fastConfig.Get<Example.Config>();
Console.WriteLine("-----Received config-----");
Console.WriteLine(appConfig);
Console.WriteLine("-------------------------");

var host = Host
  .CreateDefaultBuilder()
  .ConfigureServices((context, services) =>
  {
    services.AddFastConfig(fastConfig);

    // this service will receive a configuration
    services.AddHostedService<HostExample.ConfigService>();
  });


await host.Build().RunAsync();