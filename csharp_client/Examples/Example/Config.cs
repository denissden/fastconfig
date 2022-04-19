namespace Example;
#nullable disable
public class Config
{
    public int ServiceId { get; set; }
    public ConnectionsConfig Connections { get; set; } = new ();
    public UrlsConfig Urls { get; set; } = new ();

    public override string ToString()
    {
        return 
            $"{nameof(ServiceId)} = {ServiceId}\n" +
            $"{nameof(Connections)}: \n" +
            $"\t{nameof(Connections.Database)} = {Connections?.Database}\n" +
            $"\t{nameof(Connections.RabbitMQ)} = {Connections?.RabbitMQ}\n" +
            $"{nameof(Urls)}: \n" +
            $"\t{nameof(Urls.Api)} = {Urls?.Api}\n" +
            $"\t{nameof(Urls.Auth)} = {Urls?.Auth}\n";
    }
}

public class ConnectionsConfig
{
    public string Database { get; set; }
    public string RabbitMQ { get; set; }
}

public class UrlsConfig
{
    public string Api { get; set; }
    public string Auth { get; set; }
}