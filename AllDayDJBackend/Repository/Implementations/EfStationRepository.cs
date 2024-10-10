using AllDayDJBackend.Database;
using AllDayDJBackend.Models;
using Microsoft.EntityFrameworkCore;

namespace AllDayDJBackend.Repository;

public class EfStationRepository : IStationRepository
{
    private ILogger<EfStationRepository> logger;
    private AllDayDJContext dbContext;
    private bool disposed = false;

    public EfStationRepository(ILogger<EfStationRepository> logger, AllDayDJContext dbContext)
    {
        this.logger = logger;
        this.dbContext = dbContext;
    }

    public Station Get(Guid id)
    {
        return dbContext.Stations.First(st => st.Id == id);
    }

    public void Update(Station station)
    {
        dbContext.Stations.Update(station);
    }

    public void Delete(Station station)
    {
        dbContext.Stations.Remove(station);
    }
    
    public List<Station> GetList(int offset, int limit)
    {
        return dbContext.Stations.OrderBy(st => st.Name).Skip(offset).Take(limit).ToList();
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