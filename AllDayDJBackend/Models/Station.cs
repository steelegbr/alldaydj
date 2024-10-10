using Microsoft.EntityFrameworkCore;   

namespace AllDayDJBackend.Models;

[Index(nameof(Name), IsUnique = true)]
public class Station
{
    public Guid Id { get; set; }
    public string Name { get; set; }
}