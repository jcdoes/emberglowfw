import django_tables2 as tables
from django.utils.html import format_html


class rule_table(tables.Table):
    Name = tables.Column()
    Source = tables.Column()
    Destination = tables.Column()
    Port = tables.Column()
    Reviewed = tables.Column()
    Reviewed_by = tables.Column()
    Approved = tables.Column()

    def render_Name(self, value, record):
        return format_html(
            '<span class="editable" data-pk="{}" data-name="editable_name">{}</span>',
            record['Name'], value
        )

    def render_Source(self, value, record):
        return format_html(
            '<span class="editable" data-pk="{}" data-name="editable_source">{}</span>',
            record['Source'], value
        )
    def render_Destination(self, value, record):
        return format_html(
            '<span class="editable" data-pk="{}" data-name="editable_dest">{}</span>',
            record['Destination'], value
        )