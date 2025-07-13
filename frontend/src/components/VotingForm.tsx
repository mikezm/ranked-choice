import React, { useState, useEffect } from 'react';
import { useCreateVoter } from '../hooks/useVoterMutations';
import { Ballot } from '../services/ballotService';
import { Vote } from '../services/voterService';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpLong, faDownLong, faX } from '@fortawesome/free-solid-svg-icons';

interface VotingFormProps {
  ballot: Ballot;
  selectedChoiceId?: number | null;
  onChoiceSelected?: (choiceId: number | null) => void;
}

const VotingForm: React.FC<VotingFormProps> = ({ ballot, selectedChoiceId, onChoiceSelected }) => {
  const [voterName, setVoterName] = useState('');
  const [selectedChoices, setSelectedChoices] = useState<Vote[]>([]);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const createVoterMutation = useCreateVoter();

  const removeChoice = (index: number) => {
    const newSelectedChoices = [...selectedChoices];
    newSelectedChoices.splice(index, 1);

    // Update ranks for remaining choices
    const updatedChoices = newSelectedChoices.map((vote, idx) => ({
      ...vote,
      rank: idx + 1,
    }));

    setSelectedChoices(updatedChoices);
  };

  useEffect(() => {
    if (selectedChoiceId) {
      const existingIndex = selectedChoices.findIndex(vote => vote.choice_id === selectedChoiceId);
      if (existingIndex < 0) {
        const newRank = selectedChoices.length + 1;
        setSelectedChoices([...selectedChoices, { choice_id: selectedChoiceId, rank: newRank }]);
      }
      if (onChoiceSelected) {
        onChoiceSelected(null);
      }
    }
  }, [selectedChoiceId, onChoiceSelected, selectedChoices]);

  const moveChoice = (index: number, direction: 'up' | 'down') => {
    if (
      (direction === 'up' && index === 0) ||
      (direction === 'down' && index === selectedChoices.length - 1)
    ) {
      return;
    }

    const newSelectedChoices = [...selectedChoices];
    const swapIndex = direction === 'up' ? index - 1 : index + 1;

    // Swap the items
    [newSelectedChoices[index], newSelectedChoices[swapIndex]] = [
      newSelectedChoices[swapIndex],
      newSelectedChoices[index],
    ];

    // Update ranks
    const updatedChoices = newSelectedChoices.map((vote, idx) => ({
      ...vote,
      rank: idx + 1,
    }));

    setSelectedChoices(updatedChoices);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!voterName.trim()) {
      alert('Please enter your name');
      return;
    }

    if (selectedChoices.length === 0) {
      alert('Please select at least one choice');
      return;
    }

    createVoterMutation.mutate(
      {
        name: voterName,
        ballot_id: ballot.id,
        votes: selectedChoices,
      },
      {
        onSuccess: () => {
          setIsSubmitted(true);
        },
      }
    );
  };

  const getChoiceName = (choiceId: number) => {
    const choice = ballot.choices.find(c => c.id === choiceId);
    return choice ? choice.name : '';
  };

  if (isSubmitted) {
    return (
      <div className="voting-form-success">
        <h2>Thank you for voting!</h2>
        <p>Your vote has been recorded.</p>
      </div>
    );
  }

  if (createVoterMutation.isError) {
    return (
      <div className="voting-form-error">
        <h2>Error</h2>
        <p>There was an error submitting your vote. Please try again.</p>
        <button onClick={() => createVoterMutation.reset()}>Try Again</button>
      </div>
    );
  }

  return (
    <div className="voting-form">
      <h2>Cast Your Vote</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="voter-name">Your Name:</label>
          <input
            id="voter-name"
            type="text"
            value={voterName}
            onChange={e => setVoterName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <h3>Your Ranked Choices:</h3>
          {selectedChoices.length === 0 ? (
            <p>Click on choices to add them to your ranking</p>
          ) : (
            <ul className="ranked-choices">
              {selectedChoices.map((vote, index) => (
                <li key={vote.choice_id} className="ranked-choice-item">
                  <span className="rank">{vote.rank}.</span>
                  <span className="choice-name">{getChoiceName(vote.choice_id)}</span>
                  <div className="rank-controls">
                    <button
                      type="button"
                      onClick={() => moveChoice(index, 'up')}
                      disabled={index === 0}
                      data-testid="up-btn"
                    >
                      <FontAwesomeIcon icon={faUpLong} />
                    </button>
                    <button
                      type="button"
                      onClick={() => moveChoice(index, 'down')}
                      disabled={index === selectedChoices.length - 1}
                      data-testid="down-btn"
                    >
                      <FontAwesomeIcon icon={faDownLong} />
                    </button>
                    <button
                      type="button"
                      onClick={() => removeChoice(index)}
                      className="remove-choice-button"
                      aria-label="Remove Choice"
                    >
                      <FontAwesomeIcon icon={faX} />
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <button
          type="submit"
          className="submit-vote-button"
          disabled={createVoterMutation.isLoading}
        >
          {createVoterMutation.isLoading ? 'Submitting...' : 'Submit Vote'}
        </button>
      </form>
    </div>
  );
};

export default VotingForm;
