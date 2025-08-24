/**
 * Route guard that allows access only when the user is authenticated.
 * It waits for auth "hydration" (restoring session/auth state) before deciding.
 * This prevents accidental redirects to /login on hard refresh of protected routes.
 */

import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

/** Protected route component that is hydration-aware. */
export default function ProtectedRoute(): JSX.Element {
  const auth = useAuth();
  const loc = useLocation();

  // Be tolerant if the context doesn't expose `hydrated` yet.
  const isHydrated =
    (auth as { hydrated?: boolean }).hydrated === undefined
      ? true
      : (auth as { hydrated?: boolean }).hydrated!;

  if (!isHydrated) {
    // Minimal placeholder while restoring auth from the server/session.
    return (
      <div role="status" aria-live="polite" style={{ padding: 16 }}>
        Loading…
      </div>
    );
  }

  return auth.isAuthed ? (
    <Outlet />
  ) : (
    <Navigate to="/login" state={{ from: loc }} replace />
  );
}
