using System.Text.Json;
using System.Text;

namespace FastConfig;
public class FastConfigClient
{
    /// <summary>
    /// Environment variable for <see cref="FastConfigClient.Address"/>
    /// </summary>
    public const string EnvAddress = "FASTCONFIG_ADDRESS";
    /// <summary>
    /// Environment variable for <see cref="FastConfigClient.AppId"/>
    /// </summary>
    public const string EnvAppId = "FASTCONFIG_APPID";
    /// <summary>
    /// Environment variable for <see cref="FastConfigClient.Token"/>
    /// </summary>
    public const string EnvToken = "FASTCONFIG_TOKEN";
    private readonly HttpClient _httpClient = new HttpClient();
    /// <summary>
    /// Server address
    /// </summary>
    /// <value></value>
    public string Address { get; }
    private Uri _address => new Uri(Address);
    /// <summary>
    /// Application name/id
    /// </summary>
    /// <value></value>
    public string AppId { get; }
    /// <summary>
    /// Access token
    /// </summary>
    /// <value></value>
    public string Token { get; }

    /// <summary>
    /// Constructor
    /// </summary>
    /// <param name="address">Server address</param>
    /// <param name="appId">Application name/id</param>
    /// <param name="token">Access token</param>
    public FastConfigClient(string address, string appId, string token)
    {
        Address = address;
        AppId = appId;
        Token = token;
        _httpClient.DefaultRequestHeaders.Add("token", Token);
    }

    /// <summary>
    /// Create a new <see cref="FastConfigClient"/>
    /// from environment variables.
    /// If parameter is passed, it is not loaded from environment.
    /// </summary>
    /// <param name="address">Server address</param>
    /// <param name="appId">Application name/id</param>
    /// <param name="token">Access token</param>
    /// <returns>Instance of <see cref="FastConfigClient"/></returns>
    public static FastConfigClient FromEnvironment(
        string? address = null,
        string? appId = null,
        string? token = null
        )
    {
        if (address is null) {
            address = Environment.GetEnvironmentVariable(EnvAddress) 
            ?? throw new ArgumentException("Address is null");
        }
        if (appId is null) {
            appId = Environment.GetEnvironmentVariable(EnvAppId) 
            ?? throw new ArgumentException("AppId is null");
        }
        if (token is null) {
            token = Environment.GetEnvironmentVariable(EnvToken) 
            ?? throw new ArgumentException("Token is null");
        }
        return new FastConfigClient(address, appId, token);
    }

    private Uri _configAddress => new Uri(_address, $"configuration/{AppId}");

    /// <summary>
    /// Get configuration
    /// </summary>
    /// <returns>Json configuration as string</returns>
    public async Task<string> GetConfig()
    {
        var res = await _httpClient.GetAsync(_configAddress);
        res.EnsureSuccessStatusCode();
        return await res.Content.ReadAsStringAsync();
    }

    /// <summary>
    /// Get configuration
    /// </summary>
    /// <returns>Deserialized json configuration</returns>
    public async Task<T?> GetConfig<T>() where T: class
    {
        var string_content = await GetConfig();
        return JsonSerializer.Deserialize<T>(string_content);
    }

    /// <summary>
    /// Send configuration as json string
    /// </summary>
    /// <param name="config"></param>
    public async Task SendConfig(string config)
    {
        var content = new StringContent(config, Encoding.UTF8, "application/json");
        var res = await _httpClient.PutAsync(_configAddress, content);
        res.EnsureSuccessStatusCode();
    }

    /// <summary>
    /// Send configuration as object of type T
    /// </summary>
    /// <param name="config">Configuration class instance</param>
    /// <typeparam name="T">Configuration class</typeparam>
    public async Task SendConfig<T>(T config) where T: class
    {
        var string_content = JsonSerializer.Serialize(config);
        await SendConfig(string_content);
    }
}
