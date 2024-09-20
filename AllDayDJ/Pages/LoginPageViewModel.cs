using System.ComponentModel;
using System.Windows.Input;
using Microsoft.Extensions.Logging;

namespace AllDayDJ.Pages;

public class LoginPageViewModel : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler PropertyChanged;
    public ICommand LoginCommand { get; private set; }
    private ILogger<LoginPageViewModel> logger;
    public LoginPageViewModel(ILogger<LoginPageViewModel> logger)
    {
        this.logger = logger;
        LoginCommand = new Command(() => LoginCommandExecute());
    }

    private async void LoginCommandExecute()
    {
        try 
        {
            logger.LogInformation("Starting login process");
            WebAuthenticatorResult authenticatorResult = await WebAuthenticator.Default.AuthenticateAsync(
                new Uri("http://localhost:5228/mobileauth/Microsoft"),
                new Uri("alldaydj://")
            );

            string accessToken = authenticatorResult.AccessToken;
            logger.LogInformation("Access token is {accessToken}", accessToken);

        }
        catch (TaskCanceledException ex)
        {
            logger.LogError("Login failed. Exception: {ex}", ex);
        }
    }
}
