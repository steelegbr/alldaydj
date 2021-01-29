import { Layout } from "./pages/Layout";
import { AuthenticationProvider } from "./components/context/AuthenticationContext";
import { ThemeProvider } from "./components/context/ThemeContext";

function App() {
  return (
    <ThemeProvider>
      <AuthenticationProvider>
        <Layout />
      </AuthenticationProvider>
    </ThemeProvider>
  );
}

export default App;
