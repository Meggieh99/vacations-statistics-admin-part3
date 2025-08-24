
// Simple API client for the statistics app (uses CRA proxy to :9000).
// All calls use relative paths and include cookies for session-based auth.

export type VacationsStats = {
  pastVacations: number;
  ongoingVacations: number;
  futureVacations: number;
};

export type TotalUsers = { totalUsers: number };
export type TotalLikes = { totalLikes: number };
export type LikesDistributionItem = { destination: string; likes: number };

export type SessionInfo = {
  authenticated: boolean;
  isAdmin?: boolean;
  user?: { id: number; email: string; role?: string | null };
};

// Basic helper that fetches JSON or throws an Error with response text.
async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(path, { credentials: "include" });
  if (!res.ok) {
    throw new Error(await res.text());
  }
  return (await res.json()) as T;
}

// Basic helper that fetches JSON or throws an Error with response text + status.
async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(path, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const txt = await res.text();
    const err = new Error(txt) as Error & { status?: number };
    err.status = res.status;
    throw err;
  }
  return (await res.json()) as T;
}

// ---- Auth endpoints (session-based on :9000 via proxy) ----
export function login(email: string, password: string): Promise<{ success: boolean }> {
  return apiPost<{ success: boolean }>("/api/login/", { email, password });
}

export function logout(): Promise<{ success: boolean }> {
  return apiPost<{ success: boolean }>("/api/logout/");
}

export function getSession(): Promise<SessionInfo> {
  return apiGet<SessionInfo>("/api/session/");
}

// ---- Statistics endpoints ----
export function getVacationsStats(): Promise<VacationsStats> {
  return apiGet<VacationsStats>("/api/vacations/stats/");
}

export function getTotalUsers(): Promise<TotalUsers> {
  return apiGet<TotalUsers>("/api/users/total/");
}

export function getTotalLikes(): Promise<TotalLikes> {
  return apiGet<TotalLikes>("/api/likes/total/");
}

export function getLikesDistribution(): Promise<LikesDistributionItem[]> {
  return apiGet<LikesDistributionItem[]>("/api/likes/distribution/");
}
// src/api/auth.ts

export function checkSession(): Promise<{ authenticated: boolean }> {
  return apiGet<{ authenticated: boolean }>("/api/session/");
}
