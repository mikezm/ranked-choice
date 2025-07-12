import { useMutation } from '@tanstack/react-query';
import { createVoter, CreateVoterRequest } from '../services/voterService';

export const useCreateVoter = () => {
  return useMutation((voterData: CreateVoterRequest) => createVoter(voterData), {
    onError: error => {
      console.error('Error creating voter:', error);
    },
  });
};
