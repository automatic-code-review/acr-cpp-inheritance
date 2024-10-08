import automatic_code_review_commons as commons
import subprocess
import json

def process_ctags_output(data):
    objs = []

    for obj in data.split("\n"):
        if obj == '':
            continue

        obj = json.loads(obj)

        typeref = ''
        if 'typeref' in obj:
            typeref = obj['typeref']

        objs.append({
            'kind': obj['kind'],
            'typeref': typeref,
            'name': obj['name'],
            'path': obj['path'],
            'line': obj['line']
        })

    return objs


def get_patterns_by_kind(changes, path_source, kind):
    patterns = []

    for change in changes:
        objs = []
        if change['deleted_file']:
            continue
        new_path = path_source + '/' + change['new_path']

        data = subprocess.run(
            'ctags --output-format=json --format=2 --fields=+line ' + new_path,
            shell=True,
            capture_output=True,
            text=True,
        ).stdout

        objs.extend(process_ctags_output(data))

        for obj in objs:
            if obj['kind'] == kind:
                patterns.append(obj)

    return patterns

def review(config):
    path_source = config['path_source']
    merge = config['merge']
    changes = merge['changes']
    patterns_type = config['config']

    comments = []

    for pattern_type in patterns_type:
        patterns = get_patterns_by_kind(changes, path_source, pattern_type['kind'])

        for pattern in patterns:
            if pattern['typeref'] in pattern_type['typeref']:
                continue
            path_relative = pattern['path'].replace(path_source, "")[1:]
            descr_comment = pattern_type['message']
            descr_comment = descr_comment.replace("${NAME}", pattern['name'] )
            descr_comment = descr_comment.replace("${TYPEREF}", ', '.join(pattern_type['typeref']))
            descr_comment = descr_comment.replace("${PATH}", path_relative)
            descr_comment = descr_comment.replace("${LINE}", str(pattern['line']))

            comments.append(commons.comment_create(
                comment_id=commons.comment_generate_id(path_relative + str(pattern['line'])),
                comment_path=path_relative,
                comment_description=descr_comment,
                comment_snipset=True,
                comment_end_line=pattern['line'],
                comment_start_line=pattern['line'],
                comment_language='c++',
            ))

    return comments