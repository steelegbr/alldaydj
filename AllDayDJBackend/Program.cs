using System.Security.Claims;
using Auth0.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Logging

builder.Services.AddSerilog(
    new LoggerConfiguration()
        .WriteTo.Console()
        .CreateLogger()
);

// Authentication

// var domain = $"https://{builder.Configuration["Auth0:Domain"]}/";
// builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
//     .AddJwtBearer(
//         options => 
//         {
//             options.Authority = domain;
//             options.Audience = builder.Configuration["Auth0:Audience"];
//             options.TokenValidationParameters = new TokenValidationParameters
//             {
//                 NameClaimType = ClaimTypes.NameIdentifier
//             };
//             options.SaveToken = true;
//         }
//     );

builder.Services.AddAuth0WebAppAuthentication(
    options => {
        options.Domain = builder.Configuration["Auth0:Domain"];
        options.ClientId = builder.Configuration["Auth0:ClientId"];
        options.ClientSecret = builder.Configuration["Auth0:ClientSecret"];
    }
).WithAccessToken(
    options => {
        options.Audience = builder.Configuration["Auth0.:Audience"];
        options.UseRefreshTokens = true;
    }
);

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.Run();
