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
  await fastConfig.SendConfig(config);
  Console.WriteLine("Config sent");
}

// get configuration before configuring services
// may be useful to get connection strings
Console.WriteLine("Getting config before building the host...");
var appConfig = await fastConfig.GetConfig<Example.Config>();
Console.WriteLine("-----Received config-----");
Console.WriteLine(appConfig);
Console.WriteLine("-------------------------");

var host = Host
  .CreateDefaultBuilder()
  .ConfigureServices((context, services) =>
  {
    // add an existing FastConfigClient
    services.AddFastConfig(fastConfig);

    // create and add a new FastConfigClient 
    services.AddFastConfig(
      address: address,
      appId: appId,
      token: token
    );

    // create and add a new FastConfigClient with 
    // address, appId and token stored in environment variables 
    // services.AddFastConfig();
    /* results in exception if there are no needed environment variables */


    // create and add a new FastConfigClient with 
    // only token stored in environment variables 
    // services.AddFastConfig(
    //   address: address,
    //   appId: appId
    // );
    /* results in exception if there are no needed environment variables */

    // this service will receive a configuration
    services.AddHostedService<HostExample.ConfigService>();
  });


await host.Build().RunAsync();