using AllDayDJBackend.Models;

namespace AllDayDJBackend.Repository;

public interface IStationRepository : IDisposable
{
    public Station Get(Guid id);
    public void Update(Station station);
    public void Delete(Station station);
    public List<Station> GetList(int offset, int limit);
}