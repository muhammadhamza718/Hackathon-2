/**
 * Frontend component tests for TodoChat and TodoList components
 * Simplified version focusing on core functionality
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TodoChat from './TodoChat';
import TodoList from './TodoList';
import '@testing-library/jest-dom';

// Mock fetch API for testing
global.fetch = jest.fn();

describe('TodoList Component', () => {
  const mockTodos = [
    {
      id: 1,
      content: 'Test todo item',
      completed: false,
      created_at: '2025-01-01T00:00:00Z',
      due_date: null
    },
    {
      id: 2,
      content: 'Completed todo',
      completed: true,
      created_at: '2025-01-01T00:00:00Z',
      due_date: '2025-12-31T10:00:00Z'
    }
  ];

  test('renders without todos and shows no todos message', () => {
    render(<TodoList todos={[]} />);

    expect(screen.getByText('No todos found.')).toBeInTheDocument();
    expect(screen.getByText('Your Todos')).toBeInTheDocument();
  });

  test('renders without todos and shows no header when showHeader is false', () => {
    render(<TodoList todos={[]} showHeader={false} />);

    expect(screen.getByText('No todos found.')).toBeInTheDocument();
    expect(screen.queryByText('Your Todos')).not.toBeInTheDocument();
  });

  test('renders todo items correctly', () => {
    render(<TodoList todos={mockTodos} />);

    // Check that todo items are rendered
    expect(screen.getByText('Test todo item')).toBeInTheDocument();
    expect(screen.getByText('Completed todo')).toBeInTheDocument();

    // Check completed status
    const completedItem = screen.getByText('Completed todo').closest('.todo-item');
    expect(completedItem).toHaveClass('completed');

    // Check pending status
    const pendingItem = screen.getByText('Test todo item').closest('.todo-item');
    expect(pendingItem).not.toHaveClass('completed');

    // Check due date formatting
    expect(screen.getByText('Due: 12/31/2025')).toBeInTheDocument();
  });

  test('shows correct status indicators', () => {
    render(<TodoList todos={mockTodos} />);

    expect(screen.getByText('○ Pending')).toBeInTheDocument();
    expect(screen.getByText('✓ Completed')).toBeInTheDocument();
  });
});

describe('TodoChat Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  afterEach(() => {
    fetch.mockClear();
  });

  test('renders initial chat interface', () => {
    render(<TodoChat />);

    expect(screen.getByText('Todo Chat Assistant')).toBeInTheDocument();
    expect(screen.getByText('Ask me to add, list, complete, or manage your todos')).toBeInTheDocument();
    expect(screen.getByText('Hello! I\'m your Todo Assistant. How can I help you today?')).toBeInTheDocument();

    // Check that suggestions are available
    expect(screen.getByText('Add a new todo: Buy groceries')).toBeInTheDocument();
    expect(screen.getByText('List all my todos')).toBeInTheDocument();
    expect(screen.getByText('Mark todo #1 as completed')).toBeInTheDocument();
  });

  test('handles input changes', () => {
    render(<TodoChat />);

    const input = screen.getByPlaceholderText('Type your message here... (e.g., \'Add a todo: Buy milk\')');
    fireEvent.change(input, { target: { value: 'Test message' } });

    expect(input.value).toBe('Test message');
  });

  test('handles suggestion button clicks', () => {
    render(<TodoChat />);

    const suggestionBtn = screen.getByText('Add a new todo: Buy groceries');
    fireEvent.click(suggestionBtn);

    const input = screen.getByPlaceholderText('Type your message here... (e.g., \'Add a todo: Buy milk\')');
    expect(input.value).toBe('Add a new todo: Buy groceries');
  });

  test('disables send button when input is empty', () => {
    render(<TodoChat />);

    const sendButton = screen.getByText('Send');
    expect(sendButton).toBeDisabled();
  });

  test('enables send button when input has text', () => {
    render(<TodoChat />);

    const input = screen.getByPlaceholderText('Type your message here... (e.g., \'Add a todo: Buy milk\')');
    fireEvent.change(input, { target: { value: 'Test message' } });

    const sendButton = screen.getByText('Send');
    expect(sendButton).not.toBeDisabled();
  });

  test('handles sending a message successfully', async () => {
    // Mock successful API response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ response: 'Todo added successfully!' })
    });

    render(<TodoChat />);

    const input = screen.getByPlaceholderText('Type your message here... (e.g., \'Add a todo: Buy milk\')');
    fireEvent.change(input, { target: { value: 'Add a new todo' } });

    const sendButton = screen.getByText('Send');
    fireEvent.click(sendButton);

    // Wait for the message to be processed
    await waitFor(() => {
      expect(screen.getByText('Add a new todo')).toBeInTheDocument();
    });

    // Check that bot response is displayed
    await waitFor(() => {
      expect(screen.getByText('Todo added successfully!')).toBeInTheDocument();
    }, { timeout: 2000 });

    // Check that input is cleared
    expect(input.value).toBe('');
  });

  test('handles API error gracefully', async () => {
    // Mock API error response
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500
    });

    render(<TodoChat />);

    const input = screen.getByPlaceholderText('Type your message here... (e.g., \'Add a todo: Buy milk\')');
    fireEvent.change(input, { target: { value: 'Test message' } });

    const sendButton = screen.getByText('Send');
    fireEvent.click(sendButton);

    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByText('Sorry, there was an error processing your request. Please try again.')).toBeInTheDocument();
    }, { timeout: 2000 });
  });

  test('handles Enter key press to send message', async () => {
    // Mock successful API response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ response: 'Message received via Enter' })
    });

    render(<TodoChat />);

    const input = screen.getByPlaceholderText('Type your message here... (e.g., \'Add a todo: Buy milk\')');
    fireEvent.change(input, { target: { value: 'Test message with enter' } });

    // Simulate Enter key press with all necessary properties
    fireEvent.keyPress(input, {
      key: 'Enter',
      code: 'Enter',
      char: '\n',
      which: 13,
      keyCode: 13
    });

    // Wait for the message to be processed
    await waitFor(() => {
      expect(screen.getByText('Test message with enter')).toBeInTheDocument();
    }, { timeout: 2000 });

    // Also wait for the bot response to ensure test isolation
    await waitFor(() => {
      expect(screen.getByText('Message received via Enter')).toBeInTheDocument();
    }, { timeout: 2000 });
  });

  test('prevents sending when loading', async () => {
    // Create a promise that resolves later to simulate loading
    const slowResponsePromise = new Promise(resolve => {
      setTimeout(() => resolve({
        ok: true,
        json: async () => ({ response: 'Delayed response' })
      }), 50);
    });

    fetch.mockResolvedValueOnce(slowResponsePromise);

    render(<TodoChat />);

    const input = screen.getByPlaceholderText('Type your message here... (e.g., \'Add a todo: Buy milk\')');
    fireEvent.change(input, { target: { value: 'Slow message' } });

    const sendButton = screen.getByText('Send');
    fireEvent.click(sendButton);

    // Try to click send button again while loading
    const sendButtonAfterClick = screen.getByText('Sending...');
    expect(sendButtonAfterClick).toBeDisabled();

    // Wait for the slow response to complete
    await waitFor(() => {
      expect(screen.getByText('Delayed response')).toBeInTheDocument();
    }, { timeout: 2000 });
  });
});