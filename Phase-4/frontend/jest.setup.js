/**
 * Jest setup for frontend testing
 */
const { expect } = require('@jest/globals');
const jestDOMMatchers = require('@testing-library/jest-dom/matchers');

// Extend Jest's expect with Testing Library's matchers
expect.extend(jestDOMMatchers);

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock Element.prototype.scrollIntoView
Element.prototype.scrollIntoView = jest.fn();

// Mock fetch API globally
global.fetch = jest.fn(() => Promise.resolve({
  ok: true,
  json: () => Promise.resolve({}),
}));