import logging
#from flask import session
#from flask_login import current_user
#from ekklesia_portal import db
#from ekklesia_portal.database.datamodel import Argument, ArgumentVote, Proposition, PropositionVote


logg = logging.getLogger(__name__)


def sijax_err(resp, msg):
    logg.error("sijax handling error: " + msg)
    resp.alert(msg)


def proposition_vote(resp, proposition_id, value):
    if not current_user.is_authenticated:
        sijax_err(resp, "not logged in, anonymous users can't vote")
        return

    # 1 means upvote, 0 revokes an earlier vote
    # downvoting would be possible, can be added later (as option)
    # could be extended to other integers if we want scored voting
    if not value in (0, 1):
        sijax_err(resp, "proposition vote value must be 0 or 1")
        return

    proposition = Proposition.query.get(proposition_id)
    if proposition is None:
        sijax_err(resp, "proposition id {} does not exist".format(proposition_id))
        return
    
    user_vote = proposition.user_vote(current_user)

    if user_vote is None:
        if value == 0:
            sijax_err(resp, "no vote found, but user wants to revoke vote")
            return

        old_value = 0
        vote = PropositionVote(proposition=proposition, user=current_user, value=value)
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

    logg.debug("%s voted %s for proposition %s, new score %s", current_user.login_name, value, proposition_id, proposition.score)
    # set new score and change voting actions
    resp.html("#proposition_score_" + str(proposition_id), proposition.score)
    resp.call("change_proposition_vote_actions", [proposition_id, old_value, value])
    
    db.session.commit()


def argument_vote(resp, argument_id, value):
    if not current_user.is_authenticated:
        sijax_err(resp, "not logged in, anonymous users can't vote")
        return

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

    logg.debug("%s voted %s for argument %s, new score %s", current_user.login_name, value, argument_id, argument.score)
    # set new score and change voting actions
    resp.html("#argument_score_" + str(argument_id), argument.score)
    resp.call("change_argument_vote_actions", [argument_id, old_value, value])
    
    db.session.commit()


def change_locale(resp, locale):
    logg.debug("user locale changed to %s", locale)
    session["locale"] = locale
    resp.call("change_locale_sijax_callback")

