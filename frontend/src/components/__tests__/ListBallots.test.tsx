import { useListBallots } from '../../hooks/useBallotQueries';
import { render, screen } from '@testing-library/react';
import ListBallots from '../ListBallots';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';

jest.mock('../../hooks/useBallotQueries');

describe('ListBallots', () => {
  const mockListBallots = useListBallots as jest.MockedFunction<typeof useListBallots>;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state', () => {
    mockListBallots.mockReturnValue({
      data: null,
      isLoading: true,
      isError: false,
      error: null,
    } as any);

    render(
      <MemoryRouter>
        <ListBallots />
      </MemoryRouter>
    );

    expect(screen.getByText('Loading ballots...')).toBeInTheDocument();
  });
  test('renders the list of ballots', () => {
    const mockBallots = [
      {
        title: 'Test Ballot One',
        slug: 'test-ballot-one',
      },
      {
        title: 'Test Ballot Two',
        slug: 'test-ballot-two',
      },
    ];
    mockListBallots.mockReturnValue({
      data: mockBallots,
      isLoading: false,
      isError: false,
      error: null,
    } as any);

    render(
      <MemoryRouter>
        <ListBallots />
      </MemoryRouter>
    );

    expect(screen.getByText('Test Ballot One')).toBeInTheDocument();
    expect(screen.getByText('Test Ballot Two')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /test ballot one/i })).toHaveAttribute(
      'href',
      '/ballot/test-ballot-one'
    );
    expect(screen.getByRole('link', { name: /test ballot two/i })).toHaveAttribute(
      'href',
      '/ballot/test-ballot-two'
    );
  });
});
