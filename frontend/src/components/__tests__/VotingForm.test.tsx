import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import VotingForm from '../VotingForm';
import { Ballot } from '../../services/ballotService';
import * as voterService from '../../services/voterService';
import '@testing-library/jest-dom';

// Mock the voterService
jest.mock('../../services/voterService');

const mockBallot: Ballot = {
  id: 1,
  title: 'Test Ballot',
  slug: 'test-ballot',
  description: 'A test ballot',
  choices: [
    { id: 101, name: 'Choice 1', description: 'Description 1' },
    { id: 102, name: 'Choice 2', description: 'Description 2' },
    { id: 103, name: 'Choice 3', description: 'Description 3' },
  ],
};

const createQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

const renderWithQueryClient = (ui: React.ReactElement) => {
  const queryClient = createQueryClient();
  return render(<QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>);
};

describe('VotingForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (voterService.createVoter as jest.Mock).mockResolvedValue('success');
  });

  it('renders the form with voter name input', () => {
    renderWithQueryClient(<VotingForm ballot={mockBallot} />);

    expect(screen.getByLabelText(/your name/i)).toBeInTheDocument();
    expect(screen.getByText(/cast your vote/i)).toBeInTheDocument();
    expect(screen.getByText(/your ranked choices/i)).toBeInTheDocument();
    expect(screen.getByText(/click on choices to add them to your ranking/i)).toBeInTheDocument();
  });

  it('handles external choice selection', async () => {
    const onChoiceSelected = jest.fn();
    const queryClient = createQueryClient();
    const { rerender } = render(
      <QueryClientProvider client={queryClient}>
        <VotingForm
          ballot={mockBallot}
          selectedChoiceId={null}
          onChoiceSelected={onChoiceSelected}
        />
      </QueryClientProvider>
    );

    // No choices should be displayed initially
    expect(screen.queryByText('Choice 1')).not.toBeInTheDocument();

    // Simulate external choice selection
    rerender(
      <QueryClientProvider client={queryClient}>
        <VotingForm
          ballot={mockBallot}
          selectedChoiceId={101}
          onChoiceSelected={onChoiceSelected}
        />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Choice 1')).toBeInTheDocument();
    });
    expect(onChoiceSelected).toHaveBeenCalledWith(null);
  });

  it('allows reordering of choices', async () => {
    const queryClient = createQueryClient();
    const { rerender } = render(
      <QueryClientProvider client={queryClient}>
        <VotingForm ballot={mockBallot} selectedChoiceId={101} />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Choice 1')).toBeInTheDocument();
    });

    rerender(
      <QueryClientProvider client={queryClient}>
        <VotingForm ballot={mockBallot} selectedChoiceId={102} />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Choice 2')).toBeInTheDocument();
    });

    const downButtons = screen.getAllByText('↓');
    fireEvent.click(downButtons[0]);

    const rankElements = screen.getAllByText(/\d+\./);
    expect(rankElements[0].textContent).toBe('1.');
    expect(rankElements[1].textContent).toBe('2.');

    const choiceElements = screen.getAllByText(/Choice \d/);
    expect(choiceElements[0].textContent).toBe('Choice 2');
    expect(choiceElements[1].textContent).toBe('Choice 1');
  });

  it('submits the form with voter data', async () => {
    renderWithQueryClient(<VotingForm ballot={mockBallot} selectedChoiceId={101} />);
    await waitFor(() => {
      expect(screen.getByText('Choice 1')).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText(/your name/i), {
      target: { value: 'Test Voter' },
    });

    fireEvent.click(screen.getByText(/submit vote/i));

    await waitFor(() => {
      expect(voterService.createVoter).toHaveBeenCalledWith({
        name: 'Test Voter',
        ballot_id: 1,
        votes: [{ choice_id: 101, rank: 1 }],
      });
    });

    await waitFor(() => {
      expect(screen.getByText(/thank you for voting/i)).toBeInTheDocument();
    });
  });

  it('shows validation error when submitting without a name', async () => {
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    renderWithQueryClient(<VotingForm ballot={mockBallot} selectedChoiceId={101} />);

    await waitFor(() => {
      expect(screen.getByText('Choice 1')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText(/submit vote/i));
    expect(alertMock).toHaveBeenCalledWith('Please enter your name');

    alertMock.mockRestore();
  });

  it('shows validation error when submitting without choices', async () => {
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    renderWithQueryClient(<VotingForm ballot={mockBallot} />);
    fireEvent.change(screen.getByLabelText(/your name/i), {
      target: { value: 'Test Voter' },
    });

    fireEvent.click(screen.getByText(/submit vote/i));

    expect(alertMock).toHaveBeenCalledWith('Please select at least one choice');

    alertMock.mockRestore();
  });
});
