from prompt_toolkit.key_binding import KeyBindings

from .root import Root


class Shell:
    def __init__(self, conn, default_prompt="> "):
        self.context = Root(conn)
        self.default_input = ""
        self.default_prompt = default_prompt

    def prompt(self):
        c = self.context
        l = [str(c)]
        while c.parent:
            l.append(str(c.parent))
            c = c.parent
        return ("/".join(reversed(l))[1:] if len(l) > 1 else "") + self.default_prompt

    def completer(self):
        return self.context.completer

    def exec(self, cmd: list):
        ret = self.context.exec(cmd)
        if ret:
            self.context = ret
        self.default_input = ""

    def bindings(self):
        b = KeyBindings()

        @b.add("?")
        def _(event):
            buf = event.current_buffer
            original_text = buf.text
            help_msg = event.app.shell.context.help(buf.text)
            buf.insert_text("?")
            buf.insert_line_below(copy_margin=False)
            buf.insert_text(help_msg)
            event.app.exit("")
            event.app.shell.default_input = original_text

        return b
