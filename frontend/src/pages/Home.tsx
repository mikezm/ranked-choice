import React, { useState } from 'react';
import BallotForm from '../components/BallotForm';
import BallotCreated from '../components/BallotCreated';
import ListBallots from '../components/ListBallots';

enum HomeState {
  INITIAL,
  CREATING_BALLOT,
  BALLOT_CREATED,
}

const Home: React.FC = () => {
  const [state, setState] = useState<HomeState>(HomeState.INITIAL);
  const [createdSlug, setCreatedSlug] = useState<string>('');

  const handleCreateBallot = () => {
    setState(HomeState.CREATING_BALLOT);
  };

  const handleBallotCreated = (slug: string) => {
    setCreatedSlug(slug);
    setState(HomeState.BALLOT_CREATED);
  };

  const handleCancel = () => {
    setState(HomeState.INITIAL);
  };

  const handleCreateAnother = () => {
    setState(HomeState.INITIAL);
  };

  return (
    <div className="home-container">
      <h1>Ranked Choice Voting App</h1>

      {state === HomeState.INITIAL && (
        <>
          <div className="welcome-section">
            <p>Welcome to the Ranked Choice Voting application!</p>
            <p>Create a new ballot to start collecting votes on your choices.</p>
            <button className="create-ballot-btn" onClick={handleCreateBallot}>
              Create New Ballot
            </button>
          </div>
          <div className="link-section">
            <ListBallots />
          </div>
        </>
      )}

      {state === HomeState.CREATING_BALLOT && (
        <BallotForm onSuccess={handleBallotCreated} onCancel={handleCancel} />
      )}

      {state === HomeState.BALLOT_CREATED && (
        <BallotCreated slug={createdSlug} onCreateAnother={handleCreateAnother} />
      )}
    </div>
  );
};

export default Home;
