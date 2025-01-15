from django_select2.forms import HeavySelect2Widget

class RedisSelect2Widget(HeavySelect2Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)