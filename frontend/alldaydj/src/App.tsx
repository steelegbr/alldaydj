import { Menu } from './components/common/Menu';
import { ThemeProvider } from './components/context/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      <>
        <Menu />
      </>
    </ThemeProvider>
  );
}

export default App;
