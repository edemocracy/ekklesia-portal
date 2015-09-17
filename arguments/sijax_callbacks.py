import logging
from flask_login import current_user
from arguments import db
from arguments.database.datamodel import Argument, ArgumentVote


logg = logging.getLogger(__name__)


def sijax_err(resp, msg):
    logg.error("sijax handling error: " + msg)
    resp.alert(msg)


def argument_vote(resp, argument_id, value):
    # 1 means upvote, -1 downvote, 0 revokes an earlier vote
    # could be extended to other integers if we want scored voting
    if not value in (-1, 0, 1):
        sijax_err(resp, "argument vote value must be -1, 0 or 1")
        return

    argument = Argument.query.get(argument_id)
    if argument is None:
        sijax_err(resp, "argument id {} does not exist".format(argument_id))
        return
    
    user_vote = argument.user_vote(current_user)

    if user_vote is None:
        if value == 0:
            sijax_err(resp, "no vote found, but user wants to revoke vote")
            return

        old_value = 0
        vote = ArgumentVote(argument=argument, user=current_user, value=value)
        db.session.add(vote)
    else:
        old_value = user_vote.value
        if value == 0:
            db.session.delete(user_vote)
        elif old_value == value:
            sijax_err(resp, "user has already voted and sent the same vote again")
            return
        else:
            user_vote.value = value

    logg.debug("%s voted %s for argument %s", current_user.login_name, value, argument_id)
    # set new score and change voting actions
    resp.html("#argument_score_" + str(argument_id), argument.score)
    resp.call("change_argument_vote_actions", [argument_id, old_value, value])
    
    db.session.commit()

