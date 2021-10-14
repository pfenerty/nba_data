from app.models import EventType

event_type_map = {
    1: 'Made Shot',
    2: 'Missed Shot',
    3: 'Free Throw',
    4: 'Rebound',
    5: 'Turnover',
    6: 'Foul',
    7: 'Violation',
    8: 'Substitution',
    9: 'Timeout',
    10: 'Jump Ball',
    11: 'Ejection',
    12: 'Period Start',
    13: 'Period End',
    18: 'Instant Replay',
    20: 'Stoppage'
}


def run():
    for pt in event_type_map:
        EventType(id=pt, name=event_type_map[pt]).save()

