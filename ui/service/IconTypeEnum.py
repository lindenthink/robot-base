from enum import Enum

import dirs


class IconTypeEnum(Enum):
    disable = dirs.join_data('close.jpg')
    running = dirs.join_data('running.jpg')
    finished = dirs.join_data('finished.jpg')
    none = None
