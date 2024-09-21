using System.ComponentModel;
using System.Windows.Input;
using AllDayDJ.Services;
using Microsoft.Extensions.Logging;

namespace AllDayDJ.Pages;

public class LoginPageViewModel : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler PropertyChanged;
    public ICommand LoginCommand { get; private set; }
    private IAuthenticationService authenticationService;

    public LoginPageViewModel(IAuthenticationService authenticationService)
    {
        this.authenticationService = authenticationService;
        LoginCommand = new Command(() => LoginCommandExecute());
    }

    private async void LoginCommandExecute()
    {
        await authenticationService.Authenticate();
    }
}
