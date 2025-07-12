import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useGetBallot } from '../hooks/useBallotQueries';
import VotingForm from '../components/VotingForm';
import '../styles/BallotDetail.css';

const BallotDetail: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const { data: ballot, isLoading, error } = useGetBallot(slug);
  const [selectedChoiceId, setSelectedChoiceId] = useState<number | null>(null);

  if (isLoading) {
    return <div className="loading">Loading ballot...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>Failed to load ballot. It may not exist or there was a server error.</p>
        <Link to="/">Return to Home</Link>
      </div>
    );
  }

  if (!ballot) {
    return (
      <div className="not-found">
        <h2>Ballot Not Found</h2>
        <p>The ballot you're looking for doesn't exist.</p>
        <Link to="/">Return to Home</Link>
      </div>
    );
  }

  const handleChoiceClick = (choiceId: number) => {
    setSelectedChoiceId(choiceId);
  };

  const handleChoiceSelected = (choiceId: number | null) => {
    setSelectedChoiceId(choiceId);
  };

  return (
    <div className="ballot-detail-container">
      <div className="ballot-header">
        <h1>{ballot.title}</h1>
        {ballot.description && <p className="ballot-description">{ballot.description}</p>}
      </div>

      <div className="ballot-content">
        <div className="choices-section">
          <h2>Choices</h2>
          <div className="choices-list">
            {ballot.choices.map(choice => (
              <div
                key={choice.id}
                className={`choice-item ${selectedChoiceId === choice.id ? 'selected' : ''}`}
                onClick={() => {
                  if (choice.id) {
                    handleChoiceClick(choice.id);
                  }
                }}
              >
                <h3>{choice.name}</h3>
                {choice.description && <p>{choice.description}</p>}
              </div>
            ))}
          </div>

          <div className="actions">
            <Link to="/" className="back-link">
              Back to Home
            </Link>
          </div>
        </div>

        <div className="voting-section">
          <VotingForm
            ballot={ballot}
            selectedChoiceId={selectedChoiceId}
            onChoiceSelected={handleChoiceSelected}
          />
        </div>
      </div>
    </div>
  );
};

export default BallotDetail;
