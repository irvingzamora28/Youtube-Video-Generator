import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  return (
    <nav className="bg-card border-b border-border shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <Link to="/" className="text-2xl font-bold text-primary">YT-Vidgen</Link>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link
                to="/"
                className={`${location.pathname === '/' ? 'border-primary text-foreground' : 'border-transparent text-muted-foreground hover:text-foreground hover:border-border'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
              >
                Dashboard
              </Link>

              <Link
                to="/projects"
                className={`${location.pathname.startsWith('/projects') ? 'border-primary text-foreground' : 'border-transparent text-muted-foreground hover:text-foreground hover:border-border'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
              >
                My Projects
              </Link>
              <Link
                to="/settings"
                className={`${location.pathname === '/settings' ? 'border-primary text-foreground' : 'border-transparent text-muted-foreground hover:text-foreground hover:border-border'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
              >
                Settings
              </Link>
            </div>
          </div>
          <div className="hidden sm:ml-6 sm:flex sm:items-center">
            <ThemeToggle />
            <div className="ml-3 relative">
              <div>
                <button
                  type="button"
                  className="bg-card flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                  id="user-menu-button"
                  aria-expanded="false"
                  aria-haspopup="true"
                >
                  <span className="sr-only">Open user menu</span>
                  <div className="h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
                    <span className="font-medium">U</span>
                  </div>
                </button>
              </div>
            </div>
          </div>
          <div className="-mr-2 flex items-center sm:hidden">
            <ThemeToggle />
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              type="button"
              className="inline-flex items-center justify-center p-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-accent focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary"
              aria-controls="mobile-menu"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              {!isMenuOpen ? (
                <svg
                  className="block h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              ) : (
                <svg
                  className="block h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {isMenuOpen && (
        <div className="sm:hidden" id="mobile-menu">
          <div className="pt-2 pb-3 space-y-1">
            <Link
              to="/"
              className={`${location.pathname === '/' ? 'bg-accent text-accent-foreground border-primary' : 'border-transparent text-foreground hover:bg-accent hover:border-border'} block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
              onClick={() => setIsMenuOpen(false)}
            >
              Dashboard
            </Link>

            <Link
              to="/projects"
              className={`${location.pathname.startsWith('/projects') ? 'bg-accent text-accent-foreground border-primary' : 'border-transparent text-foreground hover:bg-accent hover:border-border'} block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
              onClick={() => setIsMenuOpen(false)}
            >
              My Projects
            </Link>
            <Link
              to="/settings"
              className={`${location.pathname === '/settings' ? 'bg-accent text-accent-foreground border-primary' : 'border-transparent text-foreground hover:bg-accent hover:border-border'} block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
              onClick={() => setIsMenuOpen(false)}
            >
              Settings
            </Link>
          </div>
          <div className="pt-4 pb-3 border-t border-border">
            <div className="flex items-center px-4">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
                  <span className="font-medium">U</span>
                </div>
              </div>
              <div className="ml-3">
                <div className="text-base font-medium text-foreground">User</div>
                <div className="text-sm font-medium text-muted-foreground">user@example.com</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
