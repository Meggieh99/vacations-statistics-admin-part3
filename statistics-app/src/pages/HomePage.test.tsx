/**
 * HomePage tests
 *
 * Positive: verifies the home page renders the main title, subtitle, and hero image.
 * Negative: verifies navigation links are NOT rendered inside the Home component (they live in the layout).
 */

import { render, screen } from "@testing-library/react";
import HomePage from "./HomePage";

test("renders home title, subtitle and image (positive)", () => {
  render(<HomePage />);
  expect(
    screen.getByRole("heading", { name: /vacation statistics/i })
  ).toBeInTheDocument();

  expect(
    screen.getByText(/admin-only statistics collected from the vacations system/i)
  ).toBeInTheDocument();

  const img = screen.getByRole("img", { name: /statistics|analytics/i });
  expect(img).toBeInTheDocument();
});

test("does not render navigation links inside Home component (negative)", () => {
  render(<HomePage />);
  // Navbar is outside this component, so these links should not appear here.
  expect(screen.queryByRole("link", { name: /login/i })).not.toBeInTheDocument();
  expect(screen.queryByRole("link", { name: /statistics/i })).not.toBeInTheDocument();
  expect(screen.queryByRole("link", { name: /about/i })).not.toBeInTheDocument();
});
