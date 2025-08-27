// src/api/auth.ts
// Unified API client for the statistics app (supports dev and Docker via proxy)

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

// 🔁 GET helper
async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`/api${path}`, {
    credentials: "include",
  });
  if (!res.ok) {
    throw new Error(await res.text());
  }
  return (await res.json()) as T;
}

// 🔁 POST helper
async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`/api${path}`, {
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

// ---- Auth endpoints ----
export function login(email: string, password: string): Promise<{ success: boolean }> {
  return apiPost<{ success: boolean }>("/login/", { email, password });
}

export function logout(): Promise<{ success: boolean }> {
  return apiPost<{ success: boolean }>("/logout/");
}

export function getSession(): Promise<SessionInfo> {
  return apiGet<SessionInfo>("/session/");
}

export function checkSession(): Promise<{ authenticated: boolean }> {
  return apiGet<{ authenticated: boolean }>("/session/");
}

// ---- Statistics endpoints ----
export function getVacationsStats(): Promise<VacationsStats> {
  return apiGet<VacationsStats>("/vacations/stats/");
}

export function getTotalUsers(): Promise<TotalUsers> {
  return apiGet<TotalUsers>("/users/total/");
}

export function getTotalLikes(): Promise<TotalLikes> {
  return apiGet<TotalLikes>("/likes/total/");
}

export function getLikesDistribution(): Promise<LikesDistributionItem[]> {
  return apiGet<LikesDistributionItem[]>("/likes/distribution/");
}
