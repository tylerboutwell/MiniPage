from django.db.models import Max
from profiles.models import Link


def get_max_position(profile) -> int:
    existing_links = Link.objects.filter(profile=profile)
    if not existing_links.exists():
        return 1
    else:
        current_max = existing_links.aggregate(max_position=Max('position'))['max_position']
        return current_max + 1


def reorder(profile):
    existing_links = Link.objects.filter(profile=profile)
    if not existing_links.exists():
        return
    number_of_links = existing_links.count()
    new_ordering = range(1, number_of_links + 1)

    for position, link in zip(new_ordering, existing_links):
        link.position = position
        link.save()