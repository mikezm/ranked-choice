import { renderHook, waitFor, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useGetBallot, useCreateBallot, useGetBallotResults } from '../useBallotQueries';
import { getBallot, createBallot, getBallotResults, Round } from '../../services/ballotService';
import React from 'react';

jest.mock('../../services/ballotService');

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe('useBallotQueries', () => {
  const mockGetBallot = getBallot as jest.MockedFunction<typeof getBallot>;
  const mockCreateBallot = createBallot as jest.MockedFunction<typeof createBallot>;
  const mockGetBallotResults = getBallotResults as jest.MockedFunction<typeof getBallotResults>;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('useGetBallot', () => {
    test('returns ballot data when successful', async () => {
      const mockBallot = {
        title: 'Test Ballot',
        slug: 'test-slug',
        description: 'Test Description',
        choices: [
          { name: 'Option 1', description: 'First option' },
          { name: 'Option 2', description: '' },
        ],
      };

      mockGetBallot.mockResolvedValue(mockBallot as any);

      const { result } = renderHook(() => useGetBallot('test-slug'), {
        wrapper: createWrapper(),
      });

      // Initially should be in loading state
      expect(result.current.isLoading).toBe(true);

      // Wait for the query to complete
      await waitFor(() => expect(result.current.isLoading).toBe(false));

      // Should have the data
      expect(result.current.data).toEqual(mockBallot);
      expect(result.current.error).toBeNull();

      // Should have called getBallot with the slug
      expect(mockGetBallot).toHaveBeenCalledWith('test-slug');
    });

    test('returns error when API call fails', async () => {
      const mockError = new Error('API Error');
      mockGetBallot.mockRejectedValue(mockError);

      renderHook(() => useGetBallot('test-slug'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => {
        expect(mockGetBallot).toHaveBeenCalledWith('test-slug');
      });

      expect(mockGetBallot).toHaveBeenCalledWith('test-slug');
    });

    test('does not fetch when slug is undefined', async () => {
      const { result } = renderHook(() => useGetBallot(undefined), {
        wrapper: createWrapper(),
      });

      // Give the hook some time to potentially make a request
      await new Promise(resolve => setTimeout(resolve, 100));

      // Should not have called getBallot
      expect(mockGetBallot).not.toHaveBeenCalled();

      // The result should have some expected properties
      expect(result.current).toHaveProperty('data', undefined);
    });
  });

  describe('useCreateBallot', () => {
    test('creates a ballot successfully', async () => {
      const mockBallotData = {
        title: 'New Ballot',
        description: 'New Description',
        choices: [
          { name: 'Option 1', description: 'First option' },
          { name: 'Option 2', description: '' },
        ],
      };

      mockCreateBallot.mockResolvedValue('new-slug');

      const { result } = renderHook(() => useCreateBallot(), {
        wrapper: createWrapper(),
      });

      // Execute the mutation
      await act(async () => {
        result.current.mutate(mockBallotData, {
          onSuccess: data => {
            // This callback will be called when the mutation succeeds
            expect(data).toBe('new-slug');
          },
        });
      });

      // Wait for the mutation to complete
      await waitFor(() => {
        expect(mockCreateBallot).toHaveBeenCalledWith(mockBallotData);
      });

      // Should not be loading anymore
      expect(result.current.isLoading).toBe(false);

      // Should have the data in the result and no error
      expect(result.current.error).toBeNull();
    });

    test('handles error when creating a ballot fails', async () => {
      const mockBallotData = {
        title: 'New Ballot',
        description: 'New Description',
        choices: [{ name: 'Option 1', description: 'First option' }],
      };

      const mockError = new Error('API Error');
      mockCreateBallot.mockRejectedValue(mockError);

      const { result } = renderHook(() => useCreateBallot(), {
        wrapper: createWrapper(),
      });

      // Execute the mutation
      await act(async () => {
        result.current.mutate(mockBallotData, {
          onError: error => {
            // This callback will be called when the mutation fails
            expect(error).toBeTruthy();
          },
        });
      });

      // Wait for the mutation to complete
      await waitFor(() => {
        expect(mockCreateBallot).toHaveBeenCalledWith(mockBallotData);
      });

      // Should not be loading anymore
      expect(result.current.isLoading).toBe(false);

      // Data should be undefined
      expect(result.current.data).toBeUndefined();
    });
  });

  describe('useGetBallotResults', () => {
    test('returns ballot data when successful', async () => {
      const mockBallotResults = {
        winner_id: 1,
        winner_name: 'Test Winner',
        title: 'Test Ballot',
        rounds: [{ name: 'Test Choice 1', votes: 3, round_index: 1 } as Round],
      } as any;

      mockGetBallotResults.mockResolvedValue(mockBallotResults);

      const { result } = renderHook(() => useGetBallotResults('test-ballot'), {
        wrapper: createWrapper(),
      });

      expect(result.current.isLoading).toBe(true);
      await waitFor(() => expect(result.current.isLoading).toBe(false));
    });

    test('returns error when API call fails', async () => {
      const mockError = new Error('API Error');
      mockGetBallotResults.mockRejectedValue(mockError);
      renderHook(() => useGetBallotResults('test-slug'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => {
        expect(mockGetBallotResults).toHaveBeenCalledWith('test-slug');
      });
      expect(mockGetBallotResults).toHaveBeenCalledWith('test-slug');
    });
  });
});
