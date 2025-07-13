import axios from 'axios';
import { createBallot, getBallot, getBallotResults, listBallots } from '../ballotService';

// Mock axios
jest.mock('axios');
const mockAxios = axios as jest.Mocked<typeof axios>;

describe('ballotService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('createBallot', () => {
    test('creates a ballot successfully', async () => {
      const mockBallotData = {
        title: 'Test Ballot',
        description: 'Test Description',
        choices: [
          { name: 'Option 1', description: 'First option' },
          { name: 'Option 2', description: '' },
        ],
      };

      const mockResponse = {
        data: {
          slug: 'test-slug',
        },
      };

      mockAxios.post.mockResolvedValue(mockResponse);

      const result = await createBallot(mockBallotData);

      expect(mockAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/ballots/'),
        mockBallotData
      );
      expect(result).toBe('test-slug');
    });

    test('throws an error when API call fails', async () => {
      const mockBallotData = {
        title: 'Test Ballot',
        description: 'Test Description',
        choices: [{ name: 'Option 1', description: 'First option' }],
      };

      const mockError = new Error('API Error');
      mockAxios.post.mockRejectedValue(mockError);

      await expect(createBallot(mockBallotData)).rejects.toThrow(mockError);
      expect(mockAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/ballots/'),
        mockBallotData
      );
    });
  });

  describe('getBallot', () => {
    test('gets a ballot successfully', async () => {
      const mockSlug = 'test-slug';
      const mockBallot = {
        title: 'Test Ballot',
        slug: mockSlug,
        description: 'Test Description',
        choices: [
          { name: 'Option 1', description: 'First option' },
          { name: 'Option 2', description: '' },
        ],
      };

      const mockResponse = {
        data: mockBallot,
      };

      mockAxios.get.mockResolvedValue(mockResponse);

      const result = await getBallot(mockSlug);

      expect(mockAxios.get).toHaveBeenCalledWith(
        expect.stringContaining(`/api/ballots/${mockSlug}/`)
      );
      expect(result).toEqual(mockBallot);
    });

    test('throws an error when API call fails', async () => {
      const mockSlug = 'test-slug';
      const mockError = new Error('API Error');

      mockAxios.get.mockRejectedValue(mockError);

      await expect(getBallot(mockSlug)).rejects.toThrow(mockError);
      expect(mockAxios.get).toHaveBeenCalledWith(
        expect.stringContaining(`/api/ballots/${mockSlug}/`)
      );
    });
  });
  describe('listBallots', () => {
    test('gets a ballot successfully', async () => {
      const mockBallots = [
        {
          title: 'Test Ballot',
          description: 'Test Description',
          choices: [
            { name: 'Option 1', description: 'First option' },
            { name: 'Option 2', description: '' },
          ],
        },
      ];

      const mockResponse = {
        data: mockBallots,
      };

      mockAxios.get.mockResolvedValue(mockResponse);

      const result = await listBallots();

      expect(mockAxios.get).toHaveBeenCalledWith(expect.stringContaining(`/api/ballots/all/`));
      expect(result).toEqual(mockBallots);
    });

    test('throws an error when API call fails', async () => {
      const mockError = new Error('API Error');

      mockAxios.get.mockRejectedValue(mockError);

      await expect(listBallots()).rejects.toThrow(mockError);
      expect(mockAxios.get).toHaveBeenCalledWith(expect.stringContaining(`/api/ballots/all/`));
    });
  });

  describe('getBallotResults', () => {
    test('gets ballot results successfully', async () => {
      const mockBallotResults = {
        winner_id: 1,
        winner_name: 'Test Winner',
        title: 'Test Ballot',
        rounds: [{ name: 'Test Choice 1', votes: 3, round_index: 1 }],
      };

      const mockResponse = { data: mockBallotResults };
      mockAxios.get.mockResolvedValue(mockResponse);

      const result = await getBallotResults('test-ballot');

      expect(mockAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('/api/ballots/results/test-ballot/')
      );
      expect(result).toEqual(mockBallotResults);
    });

    test('throws an error when API call fails', async () => {
      const mockError = new Error('API Error');
      mockAxios.get.mockRejectedValue(mockError);

      await expect(getBallotResults('test-ballot')).rejects.toThrow(mockError);

      expect(mockAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('/api/ballots/results/test-ballot/')
      );
    });
  });
});
