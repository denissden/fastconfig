using FastConfig;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace Microsoft.Extensions.DependencyInjection;
public static class ServiceCollectionExtensions
{
  public static IServiceCollection AddFastConfig(
    this IServiceCollection services,
    FastConfigClient fastConfigClient
  )
  {
    services.TryAddSingleton<FastConfigClient>(fastConfigClient);

    return services;
  }

  /// <summary>
  /// Adds a singleton instance of <see cref="FastConfigClient"/> 
  /// to services from arguments or environment variables
  /// </summary>
  /// <returns><see cref="IServiceCollection"/></returns>
  public static IServiceCollection AddFastConfig(
    this IServiceCollection services,
    string? address = null, 
    string? appId = null, 
    string? token = null
  )
  {
    var fastConfig = FastConfigClient.FromEnvironment(address, appId, token);
    services.AddFastConfig(fastConfig);

    return services;
  }
}
