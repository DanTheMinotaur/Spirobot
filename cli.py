import click
from app.bot import Body

body = Body()


@click.group()
def cli():
    pass


@cli.command()
def mv_rfr_lg():
    click.echo('Setting Right Front Leg')
    body.move_leg({
        "position": "rightfront",
        "upper": 1,
        "lower": 4
    })

@cli.command()
def mv_rmd_lg():
    click.echo('Setting Right Front Leg')
    body.move_leg({
        "position": "rightmiddle",
        "upper": 6,
        "lower": 5
    })

@cli.command()
def mv_rbk_lg():
    click.echo('Setting Right Front Leg')
    body.move_leg({
        "position": "rightback",
        "upper": 8,
        "lower": 7
    })



@cli.command()
def mv_lfr_lg():
    click.echo('Setting Left Front Leg')
    body.move_leg({
        "position": "leftfront",
        "upper": 3,
        "lower": 2
    })


@cli.command()
def mv_lbk_lg():
    click.echo('Moving Left Back Leg')
    body.move_leg({
        "position": "leftback",
        "upper": 9,
        "lower": 10
    })


@cli.command()
def mv_lmd_lg():
    click.echo('Moving Left Back Leg')
    body.move_leg({
        "position": "leftmiddle",
        "upper": 11,
        "lower": 14
    })


@cli.command()
@click.argument('steps')
def walk_forward(steps):
    click.echo("Moving Forward")
    body.walk_forward(int(steps))

@cli.command()
def leg_up():
    click.echo("Moving Leg up")
    body.leg_up({
        "position": "leftmiddle",
        "upper": 11,
        "lower": 14
    })

@cli.command()
def leg_down():
    click.echo("Moving Leg up")
    body.leg_up({
        "position": "leftmiddle",
        "upper": 11,
        "lower": 14
    })


@cli.command()
def init():
    click.echo('Setting All Legs to Initial State')
    body.set_all_initial()


@cli.command()
@click.argument('channel')
@click.argument('angle')
def servo(channel, angle):
    body.test_servo(int(channel), int(angle))

if __name__ == '__main__':
    cli()
