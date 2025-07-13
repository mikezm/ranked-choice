import React from 'react';
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

const BallotResult: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const { data: ballotResult, isLoading } = useGetBallotResults(slug);

  if (isLoading || !ballotResult) {
    return <div className="loading">Loading ballot...</div>;
  }

  const roundsData = ballotResult.rounds.reduce((acc, round) => {
    const roundIndex = round.round_index;
    if (!acc[roundIndex]) {
      acc[roundIndex] = [];
    }
    acc[roundIndex].push(round);
    return acc;
  }, {} as Record<number, typeof ballotResult.rounds>);

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

        {Object.entries(roundsData).map(([roundIndex, choices]) => (
          <div key={roundIndex} style={{ marginBottom: '30px' }}>
            <h3>Round {parseInt(roundIndex) + 1}</h3>
            <ResponsiveContainer width="100%" height={choices.length * 60}>
              <BarChart
                data={choices}
                layout="vertical"
                margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis type="category" dataKey="name" width={80} />
                <Tooltip />
                <Legend />
                <Bar dataKey="votes" name="Votes">
                  {choices.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        ))}
      </div>
    </div>
  );
};
export default BallotResult;
