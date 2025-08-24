/**
 * Global test setup for CRA + Jest.
 * - Extends jest-dom matchers.
 * - Polyfills fetch (whatwg-fetch).
 * - Polyfills ResizeObserver for Recharts' ResponsiveContainer.
 * - Shims matchMedia (optional).
 */
import "@testing-library/jest-dom";
import "whatwg-fetch";

// Minimal ResizeObserver polyfill for jsdom
class ResizeObserverMock {
  // Keep API-compatible signature: constructor(callback: ResizeObserverCallback)
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  constructor(_callback: ResizeObserverCallback) {}
  // Keep method signatures compatible with DOM lib
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  observe(_target: Element): void {}
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  unobserve(_target: Element): void {}
  disconnect(): void {}
}

// Attach to global without TypeScript suppression comments
// eslint-disable-next-line @typescript-eslint/no-explicit-any
(globalThis as any).ResizeObserver = ResizeObserverMock;

// matchMedia shim (useful for components reading prefers-color-scheme, etc.)
if (!(window as any).matchMedia) {
  (window as any).matchMedia = () => ({
    matches: false,
    media: "",
    onchange: null,
    addListener: () => {}, // deprecated
    removeListener: () => {}, // deprecated
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  });
}
