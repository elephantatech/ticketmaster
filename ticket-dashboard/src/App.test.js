import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders today\'s tickets header', () => {
  render(<App />);
  const headerElement = screen.getByText(/today's tickets/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders summary chart header', () => {
  render(<App />);
  const headerElement = screen.getByText(/summary chart/i);
  expect(headerElement).toBeInTheDocument();
});
