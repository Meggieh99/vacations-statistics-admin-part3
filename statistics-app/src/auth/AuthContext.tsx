// src/auth/AuthContext.tsx

import React, { createContext, useContext, useEffect, useState } from "react";
import { checkSession } from "../api/auth";

type AuthContextValue = {
  isAuthed: boolean;
  loading: boolean;
  setAuthed: (value: boolean) => void;
};

/**
 * Provides global authentication state to the app.
 * Automatically checks session on initial load to persist login across refreshes.
 */
const AuthContext = createContext<AuthContextValue>({
  isAuthed: false,
  loading: true,
  setAuthed: () => {},
});

export const useAuth = (): AuthContextValue => useContext(AuthContext);

export function AuthProvider({ children }: { children: React.ReactNode }): JSX.Element {
  const [isAuthed, setAuthed] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkSession()
      .then((res) => setAuthed(res.authenticated))
      .catch(() => setAuthed(false))
      .finally(() => setLoading(false));
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthed, setAuthed, loading }}>
      {children}
    </AuthContext.Provider>
  );
}
