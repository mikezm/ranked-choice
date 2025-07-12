from typing import List, Optional, Dict
from collections import defaultdict

from ranked_choice.core.repositories.ballot_repository_interface import BallotRepositoryInterface
from ranked_choice.core.domain.items.voter_item import VoterItem
from ranked_choice.core.domain.items.ballot_item import BallotResultItem


def get_votes_workflow(
    slug: str,
    ballot_repository: Optional[BallotRepositoryInterface] = None
) -> BallotResultItem:
    ballot = ballot_repository.get_ballot_by_slug(slug=slug)
    if not ballot:
        return BallotResultItem(winner_id=-1, winner_name="No ballot found", rounds=[])

    voter_items = ballot_repository.get_votes_by_ballot_id(ballot_id=ballot.id)

    choice_name_map = {choice.id: choice.name for choice in ballot.choices}

    return calculate_ranked_choice_winner(voter_items, choice_name_map)


def calculate_ranked_choice_winner(voter_items: List[VoterItem], choice_name_map: Dict[int, str]) -> BallotResultItem:
    if not voter_items:
        return BallotResultItem(winner_id=-1, winner_name="No votes found", rounds=[])

    rounds = []
    all_choices = set()
    eliminated_choices = set()

    for voter in voter_items:
        for vote in voter.votes:
            all_choices.add(vote.choice_id)

    remaining_choices = all_choices.copy()

    while remaining_choices:
        vote_counts = defaultdict(int)
        for voter in voter_items:
            active_votes = sorted([v for v in voter.votes if v.choice_id in remaining_choices], 
                                 key=lambda v: v.rank)
            if active_votes:
                top_vote = active_votes[0]
                vote_counts[top_vote.choice_id] += 1

        if not vote_counts:
            break

        rounds.append(dict(vote_counts))
        total_votes = len(voter_items)
        majority_threshold = total_votes / 2
        max_votes = max(vote_counts.values())
        winners = [choice_id for choice_id, count in vote_counts.items() if count == max_votes]

        if max_votes > majority_threshold or len(remaining_choices) <= 1:
            winner_id = winners[0]
            return BallotResultItem(
                winner_id=winner_id,
                winner_name=choice_name_map.get(winner_id, "Unknown"),
                rounds=rounds
            )

        min_votes = min(vote_counts.values())
        losers = [choice_id for choice_id, count in vote_counts.items() if count == min_votes]

        if len(losers) == len(vote_counts) and len(remaining_choices) <= 2:
            winner_id = winners[0]
            return BallotResultItem(
                winner_id=winner_id,
                winner_name=choice_name_map.get(winner_id, "Unknown"),
                rounds=rounds
            )

        loser = losers[0]
        remaining_choices.remove(loser)
        eliminated_choices.add(loser)

    if rounds:
        last_round = rounds[-1]
        if last_round:
            max_votes = max(last_round.values())
            winners = [choice_id for choice_id, count in last_round.items() if count == max_votes]
            winner_id = winners[0]
            return BallotResultItem(
                winner_id=winner_id,
                winner_name=choice_name_map.get(winner_id, "Unknown"),
                rounds=rounds
            )

    return BallotResultItem(
        winner_id=-1,
        winner_name="No winner",
        rounds=rounds
    )
