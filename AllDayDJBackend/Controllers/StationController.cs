using AllDayDJBackend.Dto;
using AllDayDJBackend.Models;
using AllDayDJBackend.Repository;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace AllDayDJBackend.Controllers;

[Route("station")]
[ApiController]
[Authorize]
public class StationController : Controller
{
    private ILogger<StationController> logger;
    private IStationRepository stationRepository;

    public StationController(ILogger<StationController> logger, IStationRepository stationRepository)
    {
        this.logger = logger;
        this.stationRepository = stationRepository;
    }

    [HttpGet]
    public List<Station> List(PaginationDto pagination)
    {
        var offset = (pagination.Page - 1) * pagination.PageSize;
        return stationRepository.GetList(offset, pagination.PageSize);
    }

}