import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import BallotResult from '../BallotResult';
import { useGetBallotResults } from '../../hooks/useBallotQueries';
import { BallotResult as BallotResultType } from '../../services/ballotService';

jest.mock('../../hooks/useBallotQueries');

jest.mock('recharts', () => {
  const OriginalModule = jest.requireActual('recharts');
  return {
    ...OriginalModule,
    ResponsiveContainer: ({ children }: { children: React.ReactNode }) => (
      <div data-testid="mock-responsive-container">{children}</div>
    ),
    BarChart: ({ children }: { children: React.ReactNode }) => (
      <div data-testid="mock-bar-chart">{children}</div>
    ),
    Bar: ({ children }: { children: React.ReactNode }) => (
      <div data-testid="mock-bar">{children}</div>
    ),
    Cell: () => <div data-testid="mock-cell" />,
    XAxis: () => <div data-testid="mock-xaxis" />,
    YAxis: () => <div data-testid="mock-yaxis" />,
    CartesianGrid: () => <div data-testid="mock-cartesian-grid" />,
    Tooltip: () => <div data-testid="mock-tooltip" />,
    Legend: () => <div data-testid="mock-legend" />,
  };
});

jest.mock('@fortawesome/react-fontawesome', () => ({
  FontAwesomeIcon: ({ icon }: { icon: any }) => {
    const iconName = icon.iconName === 'less-than' ? 'prev-icon' : 'next-icon';
    return <div data-testid={iconName} />;
  },
}));

describe('BallotResult Component', () => {
  const mockUseGetBallotResults = useGetBallotResults as jest.MockedFunction<
    typeof useGetBallotResults
  >;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state', () => {
    mockUseGetBallotResults.mockReturnValue({
      data: undefined,
      isLoading: true,
      error: null,
      isError: false,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/results/test-slug']}>
        <Routes>
          <Route path="/ballot/results/:slug" element={<BallotResult />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Loading ballot...')).toBeInTheDocument();
  });

  test('renders ballot results when data is available', () => {
    const mockBallotResult: BallotResultType = {
      winner_id: 101,
      winner_name: 'Option 1',
      title: 'Test Ballot',
      rounds: [
        { name: 'Option 1', votes: 5, round_index: 0 },
        { name: 'Option 2', votes: 3, round_index: 0 },
        { name: 'Option 3', votes: 2, round_index: 0 },
      ],
    };

    mockUseGetBallotResults.mockReturnValue({
      data: mockBallotResult,
      isLoading: false,
      error: null,
      isError: false,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/results/test-slug']}>
        <Routes>
          <Route path="/ballot/results/:slug" element={<BallotResult />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Test Ballot Results')).toBeInTheDocument();
    expect(screen.getByText('Winner: Option 1')).toBeInTheDocument();
    expect(screen.getByText('Round 1 of 1')).toBeInTheDocument();
    expect(screen.getByText('Back to Home')).toBeInTheDocument();
    expect(screen.getByText('Ballot Votes')).toBeInTheDocument();

    expect(screen.getByTestId('mock-responsive-container')).toBeInTheDocument();
    expect(screen.getByTestId('mock-bar-chart')).toBeInTheDocument();
    expect(screen.getByTestId('mock-bar')).toBeInTheDocument();
  });

  test('handles navigation between rounds', () => {
    const mockBallotResult: BallotResultType = {
      winner_id: 101,
      winner_name: 'Option 1',
      title: 'Test Ballot',
      rounds: [
        { name: 'Option 1', votes: 5, round_index: 0 },
        { name: 'Option 2', votes: 3, round_index: 0 },
        { name: 'Option 3', votes: 2, round_index: 0 },
        { name: 'Option 1', votes: 6, round_index: 1 },
        { name: 'Option 2', votes: 4, round_index: 1 },
      ],
    };

    mockUseGetBallotResults.mockReturnValue({
      data: mockBallotResult,
      isLoading: false,
      error: null,
      isError: false,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/results/test-slug']}>
        <Routes>
          <Route path="/ballot/results/:slug" element={<BallotResult />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Round 1 of 2')).toBeInTheDocument();

    const nextButton = screen.getByTestId('next-round-btn');
    fireEvent.click(nextButton);

    expect(screen.getByText('Round 2 of 2')).toBeInTheDocument();

    const prevButton = screen.getByTestId('previous-round-btn');
    fireEvent.click(prevButton);

    expect(screen.getByText('Round 1 of 2')).toBeInTheDocument();
  });

  test('disables navigation buttons appropriately', () => {
    const mockBallotResult: BallotResultType = {
      winner_id: 101,
      winner_name: 'Option 1',
      title: 'Test Ballot',
      rounds: [
        { name: 'Option 1', votes: 5, round_index: 0 },
        { name: 'Option 2', votes: 3, round_index: 0 },
        { name: 'Option 1', votes: 6, round_index: 1 },
        { name: 'Option 2', votes: 4, round_index: 1 },
      ],
    };

    mockUseGetBallotResults.mockReturnValue({
      data: mockBallotResult,
      isLoading: false,
      error: null,
      isError: false,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/results/test-slug']}>
        <Routes>
          <Route path="/ballot/results/:slug" element={<BallotResult />} />
        </Routes>
      </MemoryRouter>
    );
    const prevButton = screen.getByTestId('previous-round-btn');
    const nextButton = screen.getByTestId('next-round-btn');

    expect(prevButton).toHaveAttribute('disabled');
    expect(nextButton).not.toHaveAttribute('disabled');

    fireEvent.click(nextButton);

    expect(prevButton).not.toHaveAttribute('disabled');
    expect(nextButton).toHaveAttribute('disabled');
  });

  test('handles empty rounds data gracefully', () => {
    const mockBallotResult: BallotResultType = {
      winner_id: 101,
      winner_name: 'Option 1',
      title: 'Test Ballot',
      rounds: [],
    };

    mockUseGetBallotResults.mockReturnValue({
      data: mockBallotResult,
      isLoading: false,
      error: null,
      isError: false,
    } as any);

    render(
      <MemoryRouter initialEntries={['/ballot/results/test-slug']}>
        <Routes>
          <Route path="/ballot/results/:slug" element={<BallotResult />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Test Ballot Results')).toBeInTheDocument();
    expect(screen.getByText('Winner: Option 1')).toBeInTheDocument();

    expect(screen.getByText('Round 1 of 0')).toBeInTheDocument();

    expect(screen.queryByTestId('mock-responsive-container')).not.toBeInTheDocument();
  });
});
