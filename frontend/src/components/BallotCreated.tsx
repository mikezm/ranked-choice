import React from 'react';
import { Link } from 'react-router-dom';

interface BallotCreatedProps {
  slug: string;
  onCreateAnother: () => void;
}

const BallotCreated: React.FC<BallotCreatedProps> = ({ slug, onCreateAnother }) => {
  return (
    <div className="ballot-created">
      <h2>Ballot Created Successfully!</h2>
      <p>Your ballot has been created and is available at:</p>
      <div className="ballot-link">
        <Link to={`/ballot/${slug}`}>{window.location.origin}/ballot/{slug}</Link>
      </div>
      <div className="actions">
        <button onClick={onCreateAnother} className="create-another-btn">
          Create Another Ballot
        </button>
      </div>
    </div>
  );
};

export default BallotCreated;