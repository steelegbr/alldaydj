using Microsoft.Extensions.Logging;

namespace AllDayDJ.Pages;

public partial class LoginPage: ContentPage
{
    public LoginPage(LoginPageViewModel viewModel)
    {
        InitializeComponent();
        BindingContext = viewModel;
    }

}