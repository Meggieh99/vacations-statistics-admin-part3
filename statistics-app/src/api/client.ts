/**
 * Minimal API client for the stats backend.
 * Supports both dev (localhost:9000) and Docker (proxy to /api).
 */

const isDev = process.env.NODE_ENV === "development"; 

export const API_BASE = isDev
  ? "http://127.0.0.1:9000"   // Dev mode (local)
  : "/api";                   // Docker mode (proxy)

/**
 * Generic API request function.
 */
async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: "include", // session cookie
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    ...init,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`${res.status} ${res.statusText} ${text}`);
  }

  return (await res.json()) as T;
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: "POST",
      body: JSON.stringify(body ?? {}),
    }),
};
