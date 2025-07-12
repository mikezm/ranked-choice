import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface Vote {
  rank: number;
  choice_id: number;
}

export interface CreateVoterRequest {
  name: string;
  ballot_id: number;
  votes: Vote[];
}

export interface CreateVoterResponse {
  status: string;
}

export const createVoter = async (voterData: CreateVoterRequest): Promise<string> => {
  try {
    const response = await axios.post<CreateVoterResponse>(`${API_URL}/api/vote/`, voterData);
    return response.data.status;
  } catch (error) {
    console.error('Error creating voter:', error);
    throw error;
  }
};
