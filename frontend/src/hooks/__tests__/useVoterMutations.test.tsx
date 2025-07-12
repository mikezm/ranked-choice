import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useCreateVoter } from '../useVoterMutations';
import * as voterService from '../../services/voterService';
import React from 'react';

// Mock the voterService
jest.mock('../../services/voterService');

const createQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

const wrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = createQueryClient();
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};

describe('useVoterMutations', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should call createVoter with the correct data', async () => {
    // Mock the createVoter function to resolve successfully
    (voterService.createVoter as jest.Mock).mockResolvedValue('success');

    // Render the hook
    const { result } = renderHook(() => useCreateVoter(), { wrapper });

    // Create test data
    const voterData = {
      name: 'Test Voter',
      ballot_id: 1,
      votes: [
        { choice_id: 101, rank: 1 },
        { choice_id: 102, rank: 2 },
      ],
    };

    // Call the mutate function
    result.current.mutate(voterData);

    // Wait for the mutation to complete
    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    // Verify that createVoter was called with the correct data
    expect(voterService.createVoter).toHaveBeenCalledWith(voterData);
  });

  it('should handle errors', async () => {
    // Mock the createVoter function to reject with an error
    const error = new Error('Failed to create voter');
    (voterService.createVoter as jest.Mock).mockRejectedValue(error);

    // Render the hook
    const { result } = renderHook(() => useCreateVoter(), { wrapper });

    // Create test data
    const voterData = {
      name: 'Test Voter',
      ballot_id: 1,
      votes: [{ choice_id: 101, rank: 1 }],
    };

    // Call the mutate function
    result.current.mutate(voterData);

    // Wait for the mutation to complete
    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    // Verify that createVoter was called with the correct data
    expect(voterService.createVoter).toHaveBeenCalledWith(voterData);
    expect(result.current.error).toBe(error);
  });
});
