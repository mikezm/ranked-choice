import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface Choice {
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
  title: string;
  slug: string;
  description: string | null;
  choices: Choice[];
}

/**
 * Create a new ballot
 * @param ballotData The ballot data to create
 * @returns Promise with the created ballot's slug
 */
export const createBallot = async (ballotData: CreateBallotRequest): Promise<string> => {
  try {
    const response = await axios.post<CreateBallotResponse>(
      `${API_URL}/api/ballots/`, 
      ballotData
    );
    return response.data.slug;
  } catch (error) {
    console.error('Error creating ballot:', error);
    throw error;
  }
};

/**
 * Get a ballot by slug
 * @param slug The ballot's slug
 * @returns Promise with the ballot data
 */
export const getBallot = async (slug: string): Promise<Ballot> => {
  try {
    const response = await axios.get<Ballot>(`${API_URL}/api/ballots/${slug}/`);
    return response.data;
  } catch (error) {
    console.error('Error getting ballot:', error);
    throw error;
  }
};