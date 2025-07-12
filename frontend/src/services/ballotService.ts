import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface Choice {
  id?: number;
  name: string;
  description: string;
}

export interface CreateBallotRequest {
  title: string;
  description?: string;
  choices: Choice[];
}

export interface CreateBallotResponse {
  slug: string;
}

export interface Ballot {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  choices: Choice[];
}

export const createBallot = async (ballotData: CreateBallotRequest): Promise<string> => {
  try {
    const response = await axios.post<CreateBallotResponse>(`${API_URL}/api/ballots/`, ballotData);
    return response.data.slug;
  } catch (error) {
    console.error('Error creating ballot:', error);
    throw error;
  }
};

export const getBallot = async (slug: string): Promise<Ballot> => {
  try {
    const response = await axios.get<Ballot>(`${API_URL}/api/ballots/${slug}/`);
    return response.data;
  } catch (error) {
    console.error('Error getting ballot:', error);
    throw error;
  }
};

export const listBallots = async (): Promise<Ballot[]> => {
  try {
    const response = await axios.get<Ballot[]>(`${API_URL}/api/ballots/all/`);
    return response.data;
  } catch (error) {
    console.error('Error listing ballots:', error);
    throw error;
  }
};
