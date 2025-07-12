import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  createBallot,
  getBallot,
  CreateBallotRequest,
  listBallots,
} from '../services/ballotService';

export const ballotKeys = {
  all: ['ballots'] as const,
  detail: (slug: string) => [...ballotKeys.all, slug] as const,
};

export const useGetBallot = (slug: string | undefined) => {
  return useQuery(ballotKeys.detail(slug || ''), () => getBallot(slug || ''), {
    enabled: !!slug,
    staleTime: 5 * 60 * 1000,
    retry: 3,
  });
};

export const useCreateBallot = () => {
  const queryClient = useQueryClient();

  return useMutation((ballotData: CreateBallotRequest) => createBallot(ballotData), {
    // Invalidate all ballot queries when a new ballot is created
    onSuccess: () => {
      queryClient.invalidateQueries(ballotKeys.all);
    },
  });
};

export const useListBallots = () => {
  return useQuery(ballotKeys.all, () => listBallots(), {
    staleTime: 5 * 60 * 1000,
    retry: 3,
  });
};
