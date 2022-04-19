using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Example;
public class CreateConfig
{
  public static Config Create()
  {
    // create and send config
    var config = new Example.Config();
    config.ServiceId = 1337;
    config.Connections.Database = "server=postgre;password=password";
    config.Connections.RabbitMQ = "server=localhost:5672;password=password";
    config.Urls.Api = "https://someapi.com/";
    config.Urls.Auth = "https://auth.someserver.com/";
    return config;
  }
}
