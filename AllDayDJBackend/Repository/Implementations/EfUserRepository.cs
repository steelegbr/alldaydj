using AllDayDJBackend.Database;
using AllDayDJBackend.Models;

namespace AllDayDJBackend.Repository;

public class EfUserRepository : IUserRepository, IDisposable
{
    private ILogger<EfUserRepository> logger;
    private AllDayDJContext dbContext;
    private bool disposed = false;

    public EfUserRepository(AllDayDJContext dbContext, ILogger<EfUserRepository> logger)
    {
        this.dbContext = dbContext;
        this.logger = logger;
    }

    public User GetOrCreateUser(string email)
    {
        var existingUser = dbContext.Users.FirstOrDefault(x => x.Email == email);
        if (existingUser != null)
        {
            logger.LogInformation("Found existing user for email {email}", email);
            return existingUser;
        }

        var user = new User
        {
            Email = email,
        };
        dbContext.Users.Add(user);

        logger.LogInformation("Created new user for email {email}", email);
        return user;
    }

    protected virtual void Dispose(bool disposing)
    {
        if (!disposed)
        {
            if (disposing)
            {
                dbContext.Dispose();
            }
            disposed = true;
        }
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

}