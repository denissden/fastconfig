using FastConfig;
using Microsoft.Extensions.Hosting;

namespace HostExample;
public class ConfigService : IHostedService
{
  private readonly FastConfigClient _client;

  public ConfigService(FastConfigClient client)
  {
    _client = client;
  }

  public async Task StartAsync(CancellationToken cancellationToken)
  {
    Console.WriteLine("Getting config from service...");
    var config = await _client.Get<Example.Config>();
    Console.WriteLine("-----Received config in service-----");
    Console.WriteLine(config);
    Console.WriteLine("------------------------------------");
  }

  public Task StopAsync(CancellationToken cancellationToken)
  {
    return Task.CompletedTask;
  }
}
