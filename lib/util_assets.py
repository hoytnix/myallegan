from os import scandir

from basehash import base62


def asset_by_id(module, id):
    base = base62()
    encoded_id = base.encode(id)

    assets = '/myallegan/myallegan/static/assets/{}'.format(module)
    files = [f.name for f in scandir(assets) if f.is_file()]

    asset_ext = None
    for file_name in files:
        if encoded_id in file_name:
            asset_ext = file_name.split('.')[-1]

    if asset_ext:
        r = '/static/assets/{module}/{id}.{ext}'
        return r.format(module=module, id=encoded_id, ext=asset_ext)
    else:
        return None
