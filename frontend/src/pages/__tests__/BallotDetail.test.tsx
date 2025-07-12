// Mock the useBallotQueries hook
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import BallotDetail from '../BallotDetail';
import { useGetBallot } from '../../hooks/useBallotQueries';

jest.mock('../../hooks/useBallotQueries');

// Mock the VotingForm component
jest.mock('../../components/VotingForm', () => {
  return {
    __esModule: true,
    default: jest.fn(({ ballot, selectedChoiceId, onChoiceSelected }) => (
      <div data-testid="mock-voting-form">
        <div>Ballot ID: {ballot.id}</div>
        <div data-testid="selected-choice-id">Selected Choice ID: {selectedChoiceId || 'none'}</div>
        <button
          data-testid="reset-choice-button"
          onClick={() => onChoiceSelected && onChoiceSelected(null)}
        >
          Reset Choice
        </button>
      </div>
    )),
  };
});

describe('BallotDetail Component', () => {
  const mockUseGetBallot = useGetBallot as jest.MockedFunction<typeof useGetBallot>;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state', () => {
    mockUseGetBallot.mockReturnValue({
      data: undefined,
      isLoading: true,
      error: null,
      isError: false,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/test-slug']}>
        <Routes>
          <Route path="/ballot/:slug" element={<BallotDetail />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Loading ballot...')).toBeInTheDocument();
  });

  test('renders error state', () => {
    mockUseGetBallot.mockReturnValue({
      data: undefined,
      isLoading: false,
      error: new Error('Failed to fetch'),
      isError: true,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/test-slug']}>
        <Routes>
          <Route path="/ballot/:slug" element={<BallotDetail />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Error')).toBeInTheDocument();
    expect(
      screen.getByText('Failed to load ballot. It may not exist or there was a server error.')
    ).toBeInTheDocument();
    expect(screen.getByText('Return to Home')).toBeInTheDocument();
  });

  test('renders not found state when data is null', () => {
    mockUseGetBallot.mockReturnValue({
      data: null,
      isLoading: false,
      error: null,
      isError: false,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/test-slug']}>
        <Routes>
          <Route path="/ballot/:slug" element={<BallotDetail />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Ballot Not Found')).toBeInTheDocument();
    expect(screen.getByText("The ballot you're looking for doesn't exist.")).toBeInTheDocument();
  });

  test('renders ballot details when data is available', () => {
    const mockBallot = {
      id: 1,
      title: 'Test Ballot',
      description: 'This is a test ballot',
      slug: 'test-slug',
      choices: [
        { id: 101, name: 'Option 1', description: 'First option' },
        { id: 102, name: 'Option 2', description: '' },
      ],
    };

    mockUseGetBallot.mockReturnValue({
      data: mockBallot,
      isLoading: false,
      error: null,
      isError: false,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/test-slug']}>
        <Routes>
          <Route path="/ballot/:slug" element={<BallotDetail />} />
        </Routes>
      </MemoryRouter>
    );

    // Check that the ballot details are displayed
    expect(screen.getByText('Test Ballot')).toBeInTheDocument();
    expect(screen.getByText('This is a test ballot')).toBeInTheDocument();
    expect(screen.getByText('Choices')).toBeInTheDocument();
    expect(screen.getByText('Option 1')).toBeInTheDocument();
    expect(screen.getByText('First option')).toBeInTheDocument();
    expect(screen.getByText('Option 2')).toBeInTheDocument();
    expect(screen.getByText('Back to Home')).toBeInTheDocument();
  });

  test('handles choice selection', () => {
    const mockBallot = {
      id: 1,
      title: 'Test Ballot',
      description: 'This is a test ballot',
      slug: 'test-slug',
      choices: [
        { id: 101, name: 'Option 1', description: 'First option' },
        { id: 102, name: 'Option 2', description: '' },
      ],
    };

    mockUseGetBallot.mockReturnValue({
      data: mockBallot,
      isLoading: false,
      error: null,
      isError: false,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/test-slug']}>
        <Routes>
          <Route path="/ballot/:slug" element={<BallotDetail />} />
        </Routes>
      </MemoryRouter>
    );

    // Check that the ballot details are displayed
    expect(screen.getByText('Test Ballot')).toBeInTheDocument();

    // Check that the choices are displayed
    const option1 = screen.getByText('Option 1');
    expect(option1).toBeInTheDocument();

    // eslint-disable-next-line testing-library/no-node-access
    expect(option1.parentElement).not.toHaveClass('selected');

    // Click on a choice
    fireEvent.click(option1);

    // eslint-disable-next-line testing-library/no-node-access
    expect(option1.parentElement).toHaveClass('selected');
  });
});
