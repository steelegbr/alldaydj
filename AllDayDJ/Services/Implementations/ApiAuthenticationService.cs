using AllDayDJ.Constants;
using Microsoft.Extensions.Logging;

namespace AllDayDJ.Services;

public class ApiAuthenticationService : IAuthenticationService
{
    public string AccessToken { get; private set; }
    public string RefreshToken { get; private set; }

    private ILogger<ApiAuthenticationService> logger;

    public ApiAuthenticationService(ILogger<ApiAuthenticationService> logger)
    {
        this.logger = logger;
    }

    public async Task<bool> Authenticate()
    {
        try 
        {
            logger.LogInformation("Starting login process");
            WebAuthenticatorResult authenticatorResult = await WebAuthenticator.Default.AuthenticateAsync(
                new Uri($"{ApiConstants.BaseUrl}/mobileauth/Auth0"),
                new Uri("alldaydj://")
            );

            AccessToken = authenticatorResult.AccessToken;
            RefreshToken = authenticatorResult.RefreshToken;
            logger.LogInformation("Successful login until {expires}", authenticatorResult.ExpiresIn);
            return true;

        }
        catch (TaskCanceledException ex)
        {
            logger.LogError("Login failed. Exception: {ex}", ex);
            return false;
        }
    }

}