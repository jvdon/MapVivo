import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Dashboard from './pages/Dashboard/index.tsx';
import { ThemeProvider } from './components/ui/theme-provider.tsx';

const router = createBrowserRouter([
  {
    path:"/",
    element: <App/>
  },
  {
    path:"/dashboard",
    element: <Dashboard/>
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider defaultTheme="dark">
      <RouterProvider router={router} />
    </ThemeProvider>
  </StrictMode>,
)
