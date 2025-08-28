/**
 *
 * Positive: admin login success triggers authentication via context.
 * Negative: non-admin or invalid credentials show a 403-like error and do NOT authenticate.
 *
 * Extra Positive: renders the email & password fields and the submit button.
 * Extra Negative: shows a generic backend error message (e.g., 500) if the login API rejects.
 */

import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import userEvent from "@testing-library/user-event";
import LoginPage from "./LoginPage";

// --- Mock the API called by the page ---
jest.mock("../api/auth", () => ({ login: jest.fn() }));
import { login } from "../api/auth";

// --- Mock the auth hook (do NOT use Provider) ---
jest.mock("../auth/AuthContext", () => ({
  useAuth: jest.fn(),
}));
import { useAuth } from "../auth/AuthContext";

// Small helper
async function fillAndSubmit(email: string, password: string) {
  await userEvent.type(screen.getByLabelText(/email/i), email);
  await userEvent.type(screen.getByLabelText(/password/i), password);
  await userEvent.click(screen.getByRole("button", { name: /login/i }));
}

beforeEach(() => {
  jest.clearAllMocks();
  (useAuth as jest.Mock).mockReturnValue({ isAuthed: false, setAuthed: jest.fn() });
});

test("admin login success authenticates (positive)", async () => {
  (login as jest.Mock).mockResolvedValue({ success: true });
  const setAuthed = jest.fn();
  (useAuth as jest.Mock).mockReturnValue({ isAuthed: false, setAuthed });

  render(
    <MemoryRouter initialEntries={["/login"]}>
      <LoginPage />
    </MemoryRouter>
  );

  await fillAndSubmit("admin@example.com", "secret");
  await waitFor(() => expect(setAuthed).toHaveBeenCalledWith(true));
});

test("non-admin or bad credentials shows 403-like error and does not authenticate (negative)", async () => {
  (login as jest.Mock).mockRejectedValue(new Error("Forbidden (403) — admin only"));
  const setAuthed = jest.fn();
  (useAuth as jest.Mock).mockReturnValue({ isAuthed: false, setAuthed });

  render(
    <MemoryRouter initialEntries={["/login"]}>
      <LoginPage />
    </MemoryRouter>
  );

  await fillAndSubmit("user@example.com", "password");
  expect(await screen.findByText(/forbidden|403|admin only/i)).toBeInTheDocument();
  expect(setAuthed).not.toHaveBeenCalled();
});

test("renders form controls (extra positive)", () => {
  render(
    <MemoryRouter initialEntries={["/login"]}>
      <LoginPage />
    </MemoryRouter>
  );

  expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
});

test("shows generic backend error message on failure (extra negative)", async () => {
  (login as jest.Mock).mockRejectedValue(new Error("Server error (500)"));
  const setAuthed = jest.fn();
  (useAuth as jest.Mock).mockReturnValue({ isAuthed: false, setAuthed });

  render(
    <MemoryRouter initialEntries={["/login"]}>
      <LoginPage />
    </MemoryRouter>
  );

  await userEvent.type(screen.getByLabelText(/email/i), "user@example.com");
  await userEvent.type(screen.getByLabelText(/password/i), "secret");
  await userEvent.click(screen.getByRole("button", { name: /login/i }));

  await waitFor(() => {
    expect(screen.getByText(/server error/i)).toBeInTheDocument();
  });
  expect(setAuthed).not.toHaveBeenCalled();
});
