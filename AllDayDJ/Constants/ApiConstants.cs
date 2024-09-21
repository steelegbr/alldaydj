namespace AllDayDJ.Constants;

public static class ApiConstants
{
#if DEBUG
  public static readonly string BaseUrl = "http://localhost:5173";
#else
  public static readonly string BaseUrl = "https://alldaydj.solidradio.co.uk"
#endif
}