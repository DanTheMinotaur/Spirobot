def validate_movement(movement_config):
    if isinstance(movement_config, list) and len(movement_config) > 0:  # Check if list of instructions
        print("Checked if list")
        valid_motions = ["movement", "limit", "wait"]
        for movement in movement_config:
            print(movement)
            if isinstance(movement, dict) and "instructions" in movement and "sequence" in movement:  # check if keys are correct
                if isinstance(movement["instructions"], list) and len(movement["instructions"]) > 0:
                    for motion in movement["instructions"]:
                        for key in motion:
                            if key not in valid_motions:
                                return False
                if not isinstance(movement["sequence"], list):
                    return False
    return True

movement_config = [{
            "instructions": [
                {
                    "movement": "up",
                    "limit": 0,
                    "wait": 0.1
                },
                {
                    "movement": "forward",
                    "limit": 0,
                    "wait": 0.1
                },
                {
                    "movement": "down",
                    "limit": 0,
                    "wait": 0
                }
            ],
            "sequence": [
                "rightfront",
                "rightback",
                "leftmiddle",
                "leftfront",
                "leftback",
                "rightmiddle"
            ]
        }]

print(validate_movement(movement_config))