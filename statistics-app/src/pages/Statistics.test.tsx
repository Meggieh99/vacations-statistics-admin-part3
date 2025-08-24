/**
 * Statistics page tests
 *
 * Positive: renders KPI cards with fetched numbers and mounts the chart.
 * Negative: when the API returns 401, an unauthorized banner is shown.
 *
 * Extra Positive: while data is loading, KPI placeholders ("-") are shown immediately.
 * Extra Negative: when likes distribution is an empty array (authorized), the "No data" message appears.
 */

import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Statistics from "./Statistics";

// Mock all API calls used by the page
jest.mock("../api/auth", () => ({
  getVacationsStats: jest.fn(),
  getTotalUsers: jest.fn(),
  getTotalLikes: jest.fn(),
  getLikesDistribution: jest.fn(),
}));
import {
  getVacationsStats,
  getTotalUsers,
  getTotalLikes,
  getLikesDistribution,
} from "../api/auth";

// ✅ Correct relative path from src/pages/* to src/auth/*
jest.mock("../auth/AuthContext", () => ({
  useAuth: jest.fn(),
}));
import { useAuth } from "../auth/AuthContext";

beforeEach(() => {
  jest.clearAllMocks();
  (useAuth as jest.Mock).mockReturnValue({ isAuthed: true, setAuthed: jest.fn() });
});

test("renders KPI cards and chart (positive)", async () => {
  (getVacationsStats as jest.Mock).mockResolvedValue({
    pastVacations: 2,
    ongoingVacations: 1,
    futureVacations: 3,
  });
  (getTotalUsers as jest.Mock).mockResolvedValue({ totalUsers: 12 });
  (getTotalLikes as jest.Mock).mockResolvedValue({ totalLikes: 7 });
  (getLikesDistribution as jest.Mock).mockResolvedValue([
    { destination: "Rome", likes: 4 },
    { destination: "Paris", likes: 2 },
    { destination: "Berlin", likes: 1 },
  ]);

  render(
    <MemoryRouter initialEntries={["/stats"]}>
      <Statistics />
    </MemoryRouter>
  );

  // Titles
  expect(await screen.findByText(/past vacations/i)).toBeInTheDocument();
  expect(screen.getByText(/ongoing vacations/i)).toBeInTheDocument();
  expect(screen.getByText(/future vacations/i)).toBeInTheDocument();
  expect(screen.getByText(/total users/i)).toBeInTheDocument();
  expect(screen.getByText(/total likes/i)).toBeInTheDocument();

  // Numbers (await the data to settle)
  expect(await screen.findByText("2")).toBeInTheDocument();
  expect(screen.getByText("1")).toBeInTheDocument();
  expect(screen.getByText("3")).toBeInTheDocument();
  expect(screen.getByText("12")).toBeInTheDocument();
  expect(screen.getByText("7")).toBeInTheDocument();

  // Recharts mounted (requires ResizeObserver polyfill in setupTests.ts)
  await waitFor(() => {
    expect(document.querySelector(".recharts-wrapper")).toBeTruthy();
  });
});

test("shows unauthorized banner on 401 (negative)", async () => {
  const e: Error & { status?: number } = new Error("Unauthorized");
  e.status = 401;

  (getVacationsStats as jest.Mock).mockRejectedValue(e);
  (getTotalUsers as jest.Mock).mockResolvedValue({ totalUsers: 0 });
  (getTotalLikes as jest.Mock).mockResolvedValue({ totalLikes: 0 });
  (getLikesDistribution as jest.Mock).mockResolvedValue([]);

  render(
    <MemoryRouter initialEntries={["/stats"]}>
      <Statistics />
    </MemoryRouter>
  );

  expect(await screen.findByText(/unauthorized/i)).toBeInTheDocument();
});

test("shows KPI placeholders while loading (extra positive)", () => {
  // Pending promises to keep the page in loading state
  (getVacationsStats as jest.Mock).mockReturnValue(new Promise(() => {}));
  (getTotalUsers as jest.Mock).mockReturnValue(new Promise(() => {}));
  (getTotalLikes as jest.Mock).mockReturnValue(new Promise(() => {}));
  (getLikesDistribution as jest.Mock).mockReturnValue(new Promise(() => {}));

  render(
    <MemoryRouter initialEntries={["/stats"]}>
      <Statistics />
    </MemoryRouter>
  );

  // Five KPI placeholders should be visible immediately
  const dashes = screen.getAllByText("-");
  expect(dashes.length).toBeGreaterThanOrEqual(5);
});

test('"No data" is shown when likes distribution is empty (extra negative)', async () => {
  (getVacationsStats as jest.Mock).mockResolvedValue({
    pastVacations: 0,
    ongoingVacations: 0,
    futureVacations: 0,
  });
  (getTotalUsers as jest.Mock).mockResolvedValue({ totalUsers: 0 });
  (getTotalLikes as jest.Mock).mockResolvedValue({ totalLikes: 0 });
  (getLikesDistribution as jest.Mock).mockResolvedValue([]);

  render(
    <MemoryRouter initialEntries={["/stats"]}>
      <Statistics />
    </MemoryRouter>
  );

  // The pie card should show "No data" when the distribution is empty
  expect(await screen.findByText(/no data/i)).toBeInTheDocument();
});
