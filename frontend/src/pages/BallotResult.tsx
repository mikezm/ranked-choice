import React, { useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';

import { useGetBallotResults } from '../hooks/useBallotQueries';
import { Link, useParams } from 'react-router-dom';
import { faLessThan, faGreaterThan } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const BallotResult: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const { data: ballotResult, isLoading } = useGetBallotResults(slug);
  const [currentRoundIndex, setCurrentRoundIndex] = useState(0);

  // Update currentRoundIndex if needed and it's the first render with data
  React.useEffect(() => {
    if (ballotResult) {
      const roundsData = ballotResult.rounds.reduce((acc, round) => {
        const roundIndex = round.round_index;
        if (!acc[roundIndex]) {
          acc[roundIndex] = [];
        }
        acc[roundIndex].push(round);
        return acc;
      }, {} as Record<number, typeof ballotResult.rounds>);

      const indices = Object.keys(roundsData)
        .map(Number)
        .sort((a, b) => a - b);

      if (indices.length > 0 && !indices.includes(currentRoundIndex)) {
        setCurrentRoundIndex(indices[0]);
      }
    }
  }, [ballotResult, currentRoundIndex]);

  if (isLoading || !ballotResult) {
    return <div className="loading">Loading ballot...</div>;
  }
  let maxVotes = 0;
  const roundsData = ballotResult.rounds.reduce((acc, round) => {
    if (round.votes > maxVotes) {
      maxVotes = round.votes;
    }
    const roundIndex = round.round_index;
    if (!acc[roundIndex]) {
      acc[roundIndex] = [];
    }
    acc[roundIndex].push(round);
    return acc;
  }, {} as Record<number, typeof ballotResult.rounds>);
  const ticks = [];
  for (let i = 0; i <= maxVotes; i++) {
    ticks.push(i);
  }

  const roundIndices = Object.keys(roundsData)
    .map(Number)
    .sort((a, b) => a - b);

  const goToPreviousRound = () => {
    const currentIndexPosition = roundIndices.indexOf(currentRoundIndex);
    if (currentIndexPosition > 0) {
      setCurrentRoundIndex(roundIndices[currentIndexPosition - 1]);
    }
  };

  const goToNextRound = () => {
    const currentIndexPosition = roundIndices.indexOf(currentRoundIndex);
    if (currentIndexPosition < roundIndices.length - 1) {
      setCurrentRoundIndex(roundIndices[currentIndexPosition + 1]);
    }
  };

  const COLORS = [
    '#8884d8',
    '#83a6ed',
    '#8dd1e1',
    '#82ca9d',
    '#a4de6c',
    '#d0ed57',
    '#ffc658',
    '#ff8042',
    '#ff5252',
    '#e57373',
  ];

  return (
    <div className="ballot-page">
      <div className="actions">
        <Link to="/" className="back-link">
          Back to Home
        </Link>
        <Link to={`/ballot/${slug}`} className="back-link">
          Ballot Votes
        </Link>
      </div>
      <div className="ballot-detail-container">
        <h2>{ballotResult.title} Results</h2>
        <p>Winner: {ballotResult.winner_name}</p>

        <div
          className="round-navigation"
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            marginBottom: '20px',
          }}
        >
          <button
            onClick={goToPreviousRound}
            disabled={roundIndices.indexOf(currentRoundIndex) === 0}
            style={{
              padding: '8px 16px',
              marginRight: '10px',
              cursor: roundIndices.indexOf(currentRoundIndex) === 0 ? 'not-allowed' : 'pointer',
              opacity: roundIndices.indexOf(currentRoundIndex) === 0 ? 0.5 : 1,
            }}
          >
            <FontAwesomeIcon icon={faLessThan} />
          </button>
          <h3>
            Round {currentRoundIndex + 1} of {roundIndices.length}
          </h3>
          <button
            onClick={goToNextRound}
            disabled={roundIndices.indexOf(currentRoundIndex) === roundIndices.length - 1}
            style={{
              padding: '8px 16px',
              marginLeft: '10px',
              cursor:
                roundIndices.indexOf(currentRoundIndex) === roundIndices.length - 1
                  ? 'not-allowed'
                  : 'pointer',
              opacity:
                roundIndices.indexOf(currentRoundIndex) === roundIndices.length - 1 ? 0.5 : 1,
            }}
          >
            <FontAwesomeIcon icon={faGreaterThan} />
          </button>
        </div>

        {roundsData[currentRoundIndex] && (
          <div style={{ marginBottom: '30px' }}>
            <ResponsiveContainer width="100%" height={roundsData[currentRoundIndex].length * 60}>
              <BarChart
                data={roundsData[currentRoundIndex]}
                layout="vertical"
                margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" ticks={ticks} />
                <YAxis type="category" dataKey="name" width={80} />
                <Tooltip />
                <Legend />
                <Bar dataKey="votes" name="Votes">
                  {roundsData[currentRoundIndex].map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
};
export default BallotResult;
