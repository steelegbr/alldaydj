using AllDayDJBackend.Models;
using Microsoft.EntityFrameworkCore;

namespace AllDayDJBackend.Database;

public class AllDayDJContext : DbContext
{
    public DbSet<User> Users { get; set; }
    public DbSet<Station> Stations { get; set; }
}