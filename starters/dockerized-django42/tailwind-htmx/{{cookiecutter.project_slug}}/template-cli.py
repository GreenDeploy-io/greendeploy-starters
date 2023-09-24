from decli import cli

data = {
    "prog": "template-cli",
    "description": "This is a template cli for django-allauth-tailwindui",
    "epilog": "And that's it",
}

parser = cli(data)
parser.parse_args()
