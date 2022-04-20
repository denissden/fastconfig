string token = ""; // insert token here
if (string.IsNullOrEmpty(token))
{
  throw new ArgumentException("Please insert a token");
}
string address = "http://localhost:5000/";
string appId = "chat";

var client = new FastConfig.FastConfigClient(address, appId, token);

if (Example.Ask.YesNo("Do you want to create an example config?"))
{
  var config = Example.CreateConfig.Create();
  await client.Send(config);
  Console.WriteLine("Config sent");
}

// get config
Console.WriteLine("Getting config");
var received = await client.Get<Example.Config>();
Console.WriteLine("-----Config-----");
Console.WriteLine(received);
Console.WriteLine("----------------");
Console.WriteLine("Success");






