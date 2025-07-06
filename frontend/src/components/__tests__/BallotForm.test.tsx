import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import BallotForm from '../BallotForm';
import { useCreateBallot } from '../../hooks/useBallotQueries';

// Mock the useBallotQueries hook
jest.mock('../../hooks/useBallotQueries');

describe('BallotForm Component', () => {
  const mockUseCreateBallot = useCreateBallot as jest.MockedFunction<typeof useCreateBallot>;
  const mockOnSuccess = jest.fn();
  const mockOnCancel = jest.fn();

  // Mock implementation of useCreateBallot
  const mockMutate = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();

    // Setup default mock implementation
    mockUseCreateBallot.mockReturnValue({
      mutate: mockMutate,
      isLoading: false,
      isError: false,
      error: null,
    } as any);
  });

  test('renders the form with initial state', () => {
    render(<BallotForm onSuccess={mockOnSuccess} onCancel={mockOnCancel} />);

    // Check form title
    expect(screen.getByText('Create New Ballot')).toBeInTheDocument();

    // Check form fields
    expect(screen.getByLabelText('Title')).toBeInTheDocument();
    expect(screen.getAllByLabelText('Description (optional)')[0]).toBeInTheDocument();
    expect(screen.getByText('Choices')).toBeInTheDocument();

    // Check initial choices (should be 2)
    const choiceHeadings = screen.getAllByText(/Choice \d+/);
    console.log('Choice headings:', choiceHeadings.length);
    expect(choiceHeadings.length).toBe(2);

    const nameLabels = screen.getAllByLabelText('Name');
    console.log('Name labels:', nameLabels.length);
    expect(nameLabels.length).toBe(2);

    const descLabels = screen.getAllByLabelText(/Description/);
    console.log('Description labels:', descLabels.length);
    expect(descLabels.length).toBe(3); // 2 for choices, 1 for ballot description

    // Check buttons
    expect(screen.getByText('Add Another Choice')).toBeInTheDocument();
    expect(screen.getByText('Cancel')).toBeInTheDocument();
    expect(screen.getByText('Create Ballot')).toBeInTheDocument();
  });

  test('validates required fields', async () => {
    render(<BallotForm onSuccess={mockOnSuccess} onCancel={mockOnCancel} />);

    fireEvent.click(screen.getByText('Create Ballot'));

    await waitFor(() => {
      expect(screen.getByText('Title is required')).toBeInTheDocument();
    });
    const choiceNameErrors = screen.getAllByText('Choice name is required');
    expect(choiceNameErrors.length).toBe(2);

    // Ensure form was not submitted
    expect(mockMutate).not.toHaveBeenCalled();
  });

  test('allows adding and removing choices', async () => {
    render(<BallotForm onSuccess={mockOnSuccess} onCancel={mockOnCancel} />);

    // Initially there should be 2 choices
    expect(screen.getAllByText(/Choice \d+/).length).toBe(2);

    fireEvent.click(screen.getByText('Add Another Choice'));

    // Now there should be 3 choices
    expect(screen.getAllByText(/Choice \d+/).length).toBe(3);

    // Remove the second choice
    const removeButtons = screen.getAllByLabelText('Remove Choice');
    fireEvent.click(removeButtons[1]);

    // Now there should be 2 choices again
    expect(screen.getAllByText(/Choice \d+/).length).toBe(2);
  });

  test('submits the form with valid data', async () => {
    render(<BallotForm onSuccess={mockOnSuccess} onCancel={mockOnCancel} />);

    // Fill in the form fields
    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Test Ballot' } });
    fireEvent.change(screen.getAllByLabelText('Description (optional)')[0], {
      target: { value: 'Test Description' },
    });

    // Get all name inputs and fill them
    const nameInputs = screen.getAllByLabelText('Name');
    fireEvent.change(nameInputs[0], { target: { value: 'Option 1' } });
    fireEvent.change(nameInputs[1], { target: { value: 'Option 2' } });

    // Get all description inputs for choices and fill the first one
    const descInputs = screen
      .getAllByLabelText(/Description/)
      .filter(el => el.id.startsWith('choices'));
    fireEvent.change(descInputs[0], { target: { value: 'First option' } });

    // Setup mock to simulate successful submission
    mockMutate.mockImplementation((data, options) => {
      options.onSuccess('test-slug');
    });

    // Submit the form
    fireEvent.click(screen.getByText('Create Ballot'));

    // Check if form was submitted with correct data
    await waitFor(() => {
      expect(mockMutate).toHaveBeenCalledWith(
        {
          title: 'Test Ballot',
          description: 'Test Description',
          choices: [
            { name: 'Option 1', description: 'First option' },
            { name: 'Option 2', description: '' },
          ],
        },
        expect.any(Object)
      );
    });

    // Check if onSuccess was called with the slug
    expect(mockOnSuccess).toHaveBeenCalledWith('test-slug');
  });

  test('handles submission error', async () => {
    render(<BallotForm onSuccess={mockOnSuccess} onCancel={mockOnCancel} />);

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Test Ballot' } });
    fireEvent.change(screen.getAllByLabelText('Name')[0], { target: { value: 'Option 1' } });
    fireEvent.change(screen.getAllByLabelText('Name')[1], { target: { value: 'Option 2' } });

    // Setup mock to simulate error
    mockMutate.mockImplementation((data, options) => {
      options.onError(new Error('API Error'));
    });

    fireEvent.click(screen.getByText('Create Ballot'));

    // Check if error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Failed to create ballot. Please try again.')).toBeInTheDocument();
    });

    // Check that onSuccess was not called
    expect(mockOnSuccess).not.toHaveBeenCalled();
  });

  test('calls onCancel when cancel button is clicked', async () => {
    render(<BallotForm onSuccess={mockOnSuccess} onCancel={mockOnCancel} />);

    fireEvent.click(screen.getByText('Cancel'));

    // Check if onCancel was called
    expect(mockOnCancel).toHaveBeenCalled();
  });
});
