/**
 * Home page (Part III): title, local image, and a short explanation.
 * Navigation is handled by the top navbar; no CTAs here.
 */

import React from "react";

/** Home page component. */
export default function HomePage(): JSX.Element {
  return (
    <main className="container home">
      <header className="home__header">
        <h1 className="home__title">Vacation Statistics</h1>
        <p className="home__subtitle home__lead">
          This portal exposes admin-only statistics collected from the vacations system.
          Sign in as an administrator to view key KPIs and interactive charts.
        </p>
      </header>

      <figure className="home__figure card">
        {/* Ensure the file exists at: public/img/stats.jpg */}
        <img
          src="/img/stats.jpg"
          alt="Analytics chart illustrating vacation statistics"
          loading="lazy"
        />
        <figcaption>Sample analytics visualization</figcaption>
      </figure>
    </main>
  );
}
