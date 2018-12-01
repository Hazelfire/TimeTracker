import sys
import json

tree = json.loads(sys.stdin.read())

def search_for_focused(node):
    if node['focused'] is True:
        return node

    for child in node['nodes']:
        focused = search_for_focused(child)
        if focused:
            return focused

    return None

sys.stdout.write(search_for_focused(tree)['window_properties']['class'])
