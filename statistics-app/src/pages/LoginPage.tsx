/**
 * Login page for the statistics frontend.
 * On success: sets client-side auth flag and navigates to /stats (or the intended page).
 * On error: shows clear messages for 401 (bad credentials) and 403 (non-admin user).
 */

import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { login } from "../api/auth";
import { useAuth } from "../auth/AuthContext";

/** Shape of react-router location state when redirected by ProtectedRoute. */
interface RedirectState {
  from?: { pathname?: string };
}

/**
 * Convert backend error (401/403) into a human-friendly message.
 *
 * @param ex - error thrown from api/auth (augmented with .status)
 * @param withCode - whether to append the HTTP status code in parentheses
 * @returns message to display to the user
 */
function normalizeLoginError(ex: unknown, withCode: boolean = true): string {
  const e = ex as (Error & { status?: number }) | undefined;
  const status = e?.status ?? 0;

  if (status === 403) return `Only admin users may log in.${withCode ? " (403)" : ""}`;
  if (status === 401) return `Invalid email or password.${withCode ? " (401)" : ""}`;

  // Fallback
  return e?.message || "Login failed. Please try again.";
}

/** Login page component. */
export default function LoginPage(): JSX.Element {
  const [email, setEmail] = useState<string>("");
  const [password, setPass] = useState<string>("");
  const [err, setErr] = useState<string>("");

  const nav = useNavigate();
  const { setAuthed } = useAuth();

  // If we came from a protected page, go back there after login; otherwise /stats
  const loc = useLocation();
  const state = (loc.state as RedirectState) || {};
  const nextPath = state.from?.pathname || "/stats";

  /** Submit handler for the login form. */
  async function onSubmit(e: React.FormEvent<HTMLFormElement>): Promise<void> {
    e.preventDefault();
    setErr("");

    try {
      const res = await login(email.trim().toLowerCase(), password);
      if (res?.success) {
        setAuthed(true);
        nav(nextPath, { replace: true });
      } else {
        setErr("Invalid email or password. (401)");
      }
    } catch (ex: unknown) {
      setErr(normalizeLoginError(ex, true));
    }
  }

  return (
    <main style={{ maxWidth: 420, margin: "32px auto", padding: "0 16px" }}>
      <h1>Login</h1>

      {err && (
        <div
          role="alert"
          style={{
            color: "#c00",
            marginBottom: 12,
            background: "#fff1f1",
            border: "1px solid #ffd7d7",
            borderRadius: 8,
            padding: "10px 12px",
          }}
        >
          {err}
        </div>
      )}

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 12 }}>
        <label>
          <div>Email</div>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            autoComplete="username"
            required
            style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #ddd" }}
          />
        </label>

        <label>
          <div>Password</div>
          <input
            value={password}
            onChange={(e) => setPass(e.target.value)}
            type="password"
            autoComplete="current-password"
            required
            style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #ddd" }}
          />
        </label>

        <button
          type="submit"
          style={{
            padding: "10px 14px",
            borderRadius: 10,
            border: "1px solid #ddd",
            background: "#2F80ED",
            color: "#fff",
            cursor: "pointer",
          }}
        >
          Login
        </button>
      </form>
    </main>
  );
}
