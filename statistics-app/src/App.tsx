/**
 * App root component that wraps all routes and providers.
 * It delays rendering until authentication state is fully hydrated.
 */

import React from "react";
import { BrowserRouter, Routes, Route, NavLink, Link, useNavigate } from "react-router-dom";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import Statistics from "./pages/Statistics";
import About from "./pages/About";
import NotFound from "./pages/NotFound";

import { AuthProvider, useAuth } from "./auth/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

import "./App.css";

/**
 * Top navigation bar component.
 * - Shows links to routes.
 * - Hides or shows items based on authentication.
 */
function Navbar(): JSX.Element {
  const { isAuthed, setAuthed } = useAuth();
  const nav = useNavigate();

  async function onLogout(): Promise<void> {
    try {
      const { logout } = await import("./api/auth");
      await logout();
    } catch {
      // ignore
    }
    setAuthed(false);
    nav("/login");
  }

  return (
    <header className="navbar" role="banner">
      <div className="navbar__inner">
        <Link to="/" className="brand">Vacations Admin</Link>
        <nav className="nav" aria-label="Main navigation">
          <NavLink to="/" end className={({ isActive }) => "nav__link" + (isActive ? " is-active" : "")}>Home</NavLink>
          {!isAuthed && (
            <NavLink to="/login" className={({ isActive }) => "nav__link" + (isActive ? " is-active" : "")}>Login</NavLink>
          )}
          {isAuthed ? (
            <NavLink to="/stats" className={({ isActive }) => "nav__link" + (isActive ? " is-active" : "")}>Statistics</NavLink>
          ) : (
            <NavLink
              to="/login"
              state={{ from: { pathname: "/stats" } }}
              className="nav__link nav__link--locked"
              title="Admin only — login required"
            >
              Statistics <span aria-hidden="true">🔒</span>
            </NavLink>
          )}
          <NavLink to="/about" className={({ isActive }) => "nav__link" + (isActive ? " is-active" : "")}>About</NavLink>
        </nav>
        {isAuthed && (
          <button type="button" className="btn btn--logout" onClick={onLogout}>Logout</button>
        )}
      </div>
    </header>
  );
}

/**
 * Wrapper to wait until AuthContext finishes checking session.
 * Prevents rendering app while loading is true.
 */
function AppContent(): JSX.Element {
  const { loading } = useAuth();

  if (loading) {
    return <div className="page-center">Loading...</div>;
  }

  return (
    <>
      <Navbar />
      <Routes>
        <Route index element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/stats" element={<Statistics />} />
        </Route>
        <Route path="/about" element={<About />} />
        <Route path="/page-not-found" element={<NotFound />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

/**
 * Top-level app component with Auth provider and router.
 */
export default function App(): JSX.Element {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </AuthProvider>
  );
}
