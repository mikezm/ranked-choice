import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { createBallot, getBallot, CreateBallotRequest } from '../services/ballotService';

// Query keys
export const ballotKeys = {
  all: ['ballots'] as const,
  detail: (slug: string) => [...ballotKeys.all, slug] as const,
};

/**
 * Hook to fetch a ballot by slug
 * @param slug The ballot's slug
 * @returns Query result with the ballot data
 */
export const useGetBallot = (slug: string | undefined) => {
  return useQuery(ballotKeys.detail(slug || ''), () => getBallot(slug || ''), {
    // Don't fetch if slug is undefined
    enabled: !!slug,
    // Keep the data fresh for 5 minutes
    staleTime: 5 * 60 * 1000,
    // Retry 3 times if the query fails
    retry: 3,
  });
};

/**
 * Hook to create a new ballot
 * @returns Mutation result with the created ballot's slug
 */
export const useCreateBallot = () => {
  const queryClient = useQueryClient();

  return useMutation((ballotData: CreateBallotRequest) => createBallot(ballotData), {
    // Invalidate all ballot queries when a new ballot is created
    onSuccess: () => {
      queryClient.invalidateQueries(ballotKeys.all);
    },
  });
};
