import json
import sys
import argparse

from workflow import Workflow, ICON_WARNING, PasswordNotFound

logger = None

parser = argparse.ArgumentParser()
parser.add_argument('--query', dest='query', type=str, default='')


def create_note(note_dict, email, password):
    logger.debug(note_dict)
    color_dict = {
        'white': gkeepapi.node.ColorValue.White,
        'red': gkeepapi.node.ColorValue.Red,
        'orange': gkeepapi.node.ColorValue.Orange,
        'yellow': gkeepapi.node.ColorValue.Yellow,
        'green': gkeepapi.node.ColorValue.Green,
        'teal': gkeepapi.node.ColorValue.Teal,
        'blue': gkeepapi.node.ColorValue.Blue,
        'darkblue': gkeepapi.node.ColorValue.DarkBlue,
        'purple': gkeepapi.node.ColorValue.Purple,
        'pink': gkeepapi.node.ColorValue.Pink,
        'brown': gkeepapi.node.ColorValue.Brown,
        'gray': gkeepapi.node.ColorValue.Gray
    }

    keep = gkeepapi.Keep()
    keep.login(email, password)

    note = keep.createNote(note_dict.get('title', ''),
                           note_dict.get('content', ''))

    if note_dict.get('color', None):
        note.color = color_dict[note_dict['color']]
    if note_dict.get('tag', None):
        label_name = note_dict.get('tag')
        label = keep.findLabel(label_name)
        if not label:
            label = keep.createLabel(label_name)
        note.labels.add(label)
    keep.sync()
    return note.id


if __name__ == u"__main__":
    wf = Workflow(libraries=['./lib'])
    logger = wf.logger
    import gkeepapi
    args = parser.parse_args()
    note = json.loads(args.query)
    email = wf.get_password('google_keep_email')
    password = wf.get_password('google_keep_password')
    note_id = create_note(note, email, password)
    sys.stdout.write("#NOTE/{}".format(note_id))
