using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Example;
public static class Ask
{
  public static bool YesNo(string question)
  {
    Console.WriteLine($"{question} [y]/n");
    var key = Console.ReadKey().KeyChar;
    Console.WriteLine();
    return key != 'N' && key != 'n';
  }
}
