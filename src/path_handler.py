from sys import argv


def path_dict(model_name, photo_dir = None):
    'returns dict of paths for structure of data folder'
    def _make_path(target):
        return "data/{}/{}".format(model_name, target)
    dd = {}
    dd['base'] = 'data/' + model_name
    dd['photo'] = photo_dir
    dd['json'] = _make_path('raw_metadata.json')
    dd['csv'] = _make_path('metadata.csv')
    dd['sframe'] = _make_path('sframe')

    return dd

if __name__ == '__main__':

    path_dict(argv[1])
