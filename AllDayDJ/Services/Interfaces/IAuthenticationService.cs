namespace AllDayDJ.Services;

public interface IAuthenticationService
{
    public string AccessToken { get; }
    public string RefreshToken { get; }
    public Task<bool> Authenticate();
}