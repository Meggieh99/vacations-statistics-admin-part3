import React, { useEffect, useMemo, useState } from "react";
import {
  getVacationsStats,
  getTotalLikes,
  getTotalUsers,
  getLikesDistribution,
  LikesDistributionItem,
} from "../api/auth";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
  PieChart,
  Pie,
  Cell as PieCell,
  Legend,
} from "recharts";

/** Professional palette (used for both bar & pie). */
const PALETTE = [
  "#2F80ED", // blue
  "#27AE60", // green
  "#F2994A", // orange
  "#9B51E0", // purple
  "#56CCF2", // light blue
  "#F2C94C", // yellow
  "#EB5757", // red
  "#6FCF97", // mint
  "#BB6BD9", // violet
  "#BDBDBD", // gray
];

function ValueTooltip({ active, payload, label }: any) {
  if (!active || !payload || !payload.length) return null;
  const p = payload[0];
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip__title">{label}</div>
      <div className="chart-tooltip__row">
        <span>Likes</span>
        <b>{p.value}</b>
      </div>
    </div>
  );
}

/** Small KPI card. */
type StatCardProps = { title: string; value?: number };
const StatCard: React.FC<StatCardProps> = ({ title, value }) => (
  <div style={{ border: "1px solid #eee", borderRadius: 12, padding: 16, minWidth: 220 }}>
    <div style={{ color: "#666", marginBottom: 8 }}>{title}</div>
    <div style={{ fontSize: 28, fontWeight: 600 }}>{value ?? "-"}</div>
  </div>
);

/** Filters state for the chart. */
type Filters = { minLikes: number; destinationQuery: string };
const defaultFilters: Filters = { minLikes: 0, destinationQuery: "" };

/** Admin-only statistics page with KPIs and charts. */
const Statistics: React.FC = () => {
  const [past, setPast] = useState<number | undefined>();
  const [ongoing, setOngoing] = useState<number | undefined>();
  const [future, setFuture] = useState<number | undefined>();
  const [totalUsers, setTotalUsers] = useState<number | undefined>();
  const [totalLikes, setTotalLikes] = useState<number | undefined>();
  const [distribution, setDistribution] = useState<LikesDistributionItem[]>([]);
  const [filters, setFilters] = useState<Filters>(defaultFilters);
  const [bannerError, setBannerError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const [v, u, l, d] = await Promise.all([
          getVacationsStats(),
          getTotalUsers(),
          getTotalLikes(),
          getLikesDistribution(),
        ]);
        setPast(v.pastVacations);
        setOngoing(v.ongoingVacations);
        setFuture(v.futureVacations);
        setTotalUsers(u.totalUsers);
        setTotalLikes(l.totalLikes);
        setDistribution(d);
        setBannerError(null);
      } catch (err) {
        const e = err as Error & { status?: number };
        if (e.status === 401) {
          setBannerError("Unauthorized — please login first.");
        } else {
          setBannerError(e.message || "Failed to fetch data.");
        }
        setPast(undefined);
        setOngoing(undefined);
        setFuture(undefined);
        setTotalUsers(undefined);
        setTotalLikes(undefined);
        setDistribution([]);
      }
    })();
  }, []);

  const filtered = useMemo<LikesDistributionItem[]>(() => {
    const q = filters.destinationQuery.trim().toLowerCase();
    return distribution
      .filter((x) => x.likes >= filters.minLikes)
      .filter((x) => (q ? x.destination.toLowerCase().includes(q) : true));
  }, [distribution, filters]);

  return (
    <main style={{ maxWidth: 1100, margin: "32px auto", padding: "0 16px" }}>
      <h1>Statistics</h1>

      {bannerError && <div style={{ color: "#c00", marginBottom: 12 }}>{bannerError}</div>}

      <section style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
        <StatCard title="Past vacations" value={past} />
        <StatCard title="Ongoing vacations" value={ongoing} />
        <StatCard title="Future vacations" value={future} />
        <StatCard title="Total users" value={totalUsers} />
        <StatCard title="Total likes" value={totalLikes} />
      </section>

      {/* Filters */}
      <section style={{ marginTop: 24 }}>
        <h2 style={{ fontSize: 18, marginBottom: 8 }}>Filters</h2>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <label>
            <span style={{ display: "block", fontSize: 12, color: "#666" }}>Min likes</span>
            <input
              type="number"
              min={0}
              value={filters.minLikes}
              onChange={(e) =>
                setFilters((f) => ({ ...f, minLikes: Number(e.target.value || 0) }))
              }
              style={{ padding: 8, borderRadius: 8, border: "1px solid #ddd", width: 120 }}
            />
          </label>

          <label>
            <span style={{ display: "block", fontSize: 12, color: "#666" }}>
              Destination contains
            </span>
            <input
              type="text"
              value={filters.destinationQuery}
              onChange={(e) => setFilters((f) => ({ ...f, destinationQuery: e.target.value }))}
              placeholder="e.g. Rome"
              style={{ padding: 8, borderRadius: 8, border: "1px solid #ddd", width: 220 }}
            />
          </label>

          <button
            onClick={() => setFilters(defaultFilters)}
            style={{
              padding: "10px 14px",
              borderRadius: 10,
              border: "1px solid #ddd",
              background: "#fafafa",
              cursor: "pointer",
            }}
          >
            Reset
          </button>
        </div>
      </section>

      {/* Bar chart */}
      <section style={{ marginTop: 24 }}>
        <h2 style={{ fontSize: 18, marginBottom: 8 }}>Likes per destination</h2>
        <div className="card" style={{ height: 360 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={filtered} margin={{ top: 8, right: 16, left: 0, bottom: 8 }}>
              <CartesianGrid vertical={false} strokeDasharray="3 3" />
              <XAxis dataKey="destination" tickMargin={8} axisLine={false} tickLine={false} />
              <YAxis allowDecimals={false} axisLine={false} tickLine={false} tickMargin={8} />
              <Tooltip content={<ValueTooltip />} />
              <Bar dataKey="likes" radius={[6, 6, 0, 0]}>
                {filtered.map((_, i) => (
                  <Cell key={`bar-${i}`} fill={PALETTE[i % PALETTE.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* Pie chart card — NEW */}
      <section style={{ marginTop: 24 }}>
        <h2 style={{ fontSize: 18, marginBottom: 8 }}>Likes share</h2>
        <div className="card" style={{ height: 340, display: "grid", placeItems: "center" }}>
          {filtered.length === 0 ? (
            <div style={{ color: "#666" }}>No data</div>
          ) : (
            <PieChart width={520} height={300}>
              <Pie
                data={filtered}
                dataKey="likes"
                nameKey="destination"
                cx={240}
                cy={140}
                innerRadius={60}
                outerRadius={100}
                paddingAngle={2}
              >
                {filtered.map((_, i) => (
                  <PieCell key={`pc-${i}`} fill={PALETTE[i % PALETTE.length]} />
                ))}
              </Pie>
              <Legend verticalAlign="bottom" height={36} />
            </PieChart>
          )}
        </div>
      </section>
    </main>
  );
};

export default Statistics;
