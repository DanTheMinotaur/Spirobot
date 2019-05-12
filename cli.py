import click
from app.bot import Movements

"""
    Script for CLI(Command Line Interfacing) of bot and communication mechanisms
"""

body = Movements()


def find_leg(leg):
    """
    Helper function to validate that selected leg is valid
    :param leg:
    :return:
    """
    selected_leg = body.select_leg(leg)
    if selected_leg is not None:
        click.echo("Using {} Leg".format(leg))
        return selected_leg
    click.echo("Could not find leg, possible choices are: ")
    for l in body.legs:
        click.echo(l["position"])
    exit()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('movement')
@click.argument('leg')
def mv_leg(movement, leg):
    """
    Move a single leg in a particular direction
    :param movement: The type of leg movement
    :param leg: the chosen leg to move
    :return:
    """
    body.leg_move(movement, find_leg(leg))


@cli.command()
@click.argument('channel')
@click.argument('angle')
def servo(channel, angle):
    """
    Move a single servo to a specific angle
    :param channel: the servo motor channel
    :param angle: the angle to move it to
    """
    body.test_servo(int(channel), int(angle))


@cli.command()
def init():
    """
    Sets all legs to starting position
    """
    click.echo('Setting All Legs to Initial State')
    body.set_all_initial()


@cli.command()
@click.argument('movement_name')
@click.argument('repeat')
def mv(movement_name, repeat=1):
    """
    Tells the bot to move to a particular movement config.
    :param movement_name: The name of the movement config
    :param repeat: The number of times to repeat the move.
    """
    body.make_move(movement_name, int(repeat), print_sequence=True)


@cli.command()
def ls_mv():
    """
    Lists all stored movement commands
    """
    click.echo('Possible Movements')
    for move in body.movements:
        click.echo(move)


if __name__ == '__main__':
    cli()
