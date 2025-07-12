import React from 'react';
import { useListBallots } from '../hooks/useBallotQueries';
import { Link } from 'react-router-dom';

const ListBallots: React.FC = () => {
  const { data: ballots, isLoading } = useListBallots();

  if (isLoading) {
    return <div className="loading">Loading ballots...</div>;
  }

  return (
    <div>
      <h2>Ballots</h2>
      {ballots &&
        ballots.map(ballot => (
          <div key={ballot.slug}>
            <Link to={`/ballot/${ballot.slug}`}>{ballot.title}</Link>
          </div>
        ))}
    </div>
  );
};

export default ListBallots;
