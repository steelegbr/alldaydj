using AllDayDJ.Pages;
using Microsoft.Extensions.Logging;
using Serilog;

namespace AllDayDJ;

public static class MauiProgram
{
	public static MauiApp CreateMauiApp()
	{
		var builder = MauiApp.CreateBuilder();
		builder
			.UseMauiApp<App>()
			.ConfigureFonts(fonts =>
			{
				fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
				fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
			});

#if DEBUG
		builder.Logging.AddDebug();
#endif

		var loggingPath = Path.Combine(Environment.GetFolderPath(System.Environment.SpecialFolder.ApplicationData), "log.txt");
		builder.Services.AddSerilog(
			new LoggerConfiguration()
				.WriteTo.File(loggingPath, rollingInterval: RollingInterval.Day)
				.CreateLogger()
			);

		builder.Services.AddSingleton<LoginPageViewModel>();
		builder.Services.AddSingleton<LoginPage>();

		return builder.Build();
	}
}
