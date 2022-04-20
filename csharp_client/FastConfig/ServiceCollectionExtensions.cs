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
}
