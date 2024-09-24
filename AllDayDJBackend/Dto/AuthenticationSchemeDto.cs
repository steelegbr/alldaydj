using System.ComponentModel.DataAnnotations;

namespace AllDayDJBackend.Dto;

public class AuthenticationSchemeDto
{
    [AllowedValues("Auth0")]
    public string Scheme { get; set; }
}