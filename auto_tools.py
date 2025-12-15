import sublime
import sublime_plugin

try:
    from . import auto_tools_core as core
except ImportError:
    import auto_tools_core as core


class AutoDecodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = [r for r in self.view.sel() if not r.empty()]
        if not regions:
            regions = [sublime.Region(0, self.view.size())]

        for region in regions:
            raw = self.view.substr(region)
            decoded = core.auto_decode_engine(raw)
            self.view.replace(edit, region, decoded)


class AutoJsonFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = [r for r in self.view.sel() if not r.empty()]
        if not regions:
            regions = [sublime.Region(0, self.view.size())]

        for region in regions:
            raw = self.view.substr(region)

            decoded = core.auto_decode_engine(raw)
            safe = core.json_sanitize(decoded)
            final = core.json_pretty(safe)

            self.view.replace(edit, region, final)
