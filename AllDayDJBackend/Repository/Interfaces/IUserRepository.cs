using AllDayDJBackend.Models;

namespace AllDayDJBackend.Repository;

public interface IUserRepository : IDisposable
{
    public User GetOrCreateUser(string email);
}