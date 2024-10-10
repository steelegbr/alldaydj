using System.Net;
using AllDayDJBackend.Dto;
using Auth0.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Mvc;

namespace AllDayDJBackend.Controllers;

// This is based on https://github.com/dotnet/maui/blob/main/src/Essentials/samples/Sample.Server.WebAuthenticator/Controllers/MobileAuthController.cs

[Route("mobileauth")]
[ApiController]
public class AuthController : ControllerBase
{
    private ILogger<AuthController> logger;

    public AuthController(ILogger<AuthController> logger)
    {
        this.logger = logger;
    }


    /// <summary>
    /// Attempts to authenticate the user. If we're already authenticated (cookie exists), the JWT 
    /// tokens from the upstream authentication service are returned. Otherwise the user is pushed
    /// into the OAuth flow.
    /// </summary>
    /// <param name="schemeDto">Indicates the authentication scheme to use.</param>
    /// <returns>A redirect, either to the MAUI app or the OAuth2 flow.</returns>

    [HttpGet("{scheme}")]
    public async Task Get([FromRoute] AuthenticationSchemeDto schemeDto)
    {
        logger.LogInformation("Authentication request for {scheme} scheme", schemeDto.Scheme);
        var auth = await Request.HttpContext.AuthenticateAsync(schemeDto.Scheme);
        logger.LogInformation("Got auth data with success={success}, principal={principal}, token={access_token}", auth.Succeeded, auth.Principal, auth.Properties.GetTokenValue("refresh_token"));

        if (!auth.Succeeded
				|| auth?.Principal == null
				|| !auth.Principal.Identities.Any(id => id.IsAuthenticated)
				|| string.IsNullOrEmpty(auth.Properties.GetTokenValue("access_token")))
        {
            logger.LogInformation("Authentication failed, challenging user");

            var authenticationProps = new LoginAuthenticationPropertiesBuilder()
                .WithRedirectUri($"/mobileauth/{schemeDto.Scheme}").Build();
            authenticationProps.IsPersistent = true;
            await Request.HttpContext.ChallengeAsync(schemeDto.Scheme, authenticationProps);
        }
        else
        {
            var claims = auth.Principal.Identities.FirstOrDefault()?.Claims;
            var email = string.Empty;
            email = claims?.FirstOrDefault(c => c.Type == System.Security.Claims.ClaimTypes.Email)?.Value;

            // Get parameters to send back to the callback
            var qs = new Dictionary<string, string>
            {
                { "access_token", auth.Properties.GetTokenValue("access_token") },
                { "refresh_token", auth.Properties.GetTokenValue("refresh_token") ?? string.Empty },
                { "expires_in", (auth.Properties.ExpiresUtc?.ToUnixTimeSeconds() ?? -1).ToString() },
                { "email", email }
            };

            // Build the result url
            var url = "alldaydj://#" + string.Join(
                "&",
                qs.Where(kvp => !string.IsNullOrEmpty(kvp.Value) && kvp.Value != "-1")
                .Select(kvp => $"{WebUtility.UrlEncode(kvp.Key)}={WebUtility.UrlEncode(kvp.Value)}"));

            // Redirect to final url
            Request.HttpContext.Response.Redirect(url);
        }

             
    }
}