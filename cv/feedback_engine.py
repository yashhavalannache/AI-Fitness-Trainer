def get_feedback(angle, config, position):

    feedback = ""

    if config["type"] == "rep":

        if angle > config["up_angle"]:

            feedback = config["feedback"]["up"]

        elif angle < config["down_angle"]:

            feedback = config["feedback"]["down"]

    elif config["type"] == "static":

        if abs(angle - config["hold_angle"]) < 15:

            feedback = config["feedback"]["good"]

        else:

            feedback = config["feedback"]["bad"]

    return feedback