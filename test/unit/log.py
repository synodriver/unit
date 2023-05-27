UNIT_LOG = 'unit.log'


class Log:
    temp_dir = None
    pos = {}

    def open(self, encoding=None):
        f = open(Log.get_path(self), 'r', encoding=encoding, errors='ignore')
        f.seek(Log.pos.get(self, 0))

        return f

    def set_pos(self, name=UNIT_LOG):
        Log.pos[name] = self

    def swap(self):
        pos = Log.pos.get(UNIT_LOG, 0)
        Log.pos[UNIT_LOG] = Log.pos.get(self, 0)
        Log.pos[self] = pos

    def get_path(self):
        return f'{Log.temp_dir}/{self}'
