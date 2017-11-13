from datagorri.view.component import Component
from datagorri.view.style import common_style as style
import tkinter


class Navigation(Component):
    def __init__(self, master_frame):
        Component.__init__(self, master_frame)
        self._tabs = {}
        self.active_tab = ''
        self.do_on_tab_click = []

    def click_at(self, label):
        if label == self.active_tab:
            return True

        if label not in list(self._tabs):
            raise KeyError('No tab "' + label + '" in navigation yet.')

        if self.active_tab in self._tabs:
            self._tabs[self.active_tab].configure(bg=style['nav']['tab']['bg'], fg=style['nav']['tab']['color'])
            self._tabs[self.active_tab].configure(bg=style['nav']['tab']['bg'], fg=style['nav']['tab']['color'], cursor="hand2")

        for function in self.do_on_tab_click:
            function(label)

        self.active_tab = label
        self._tabs[self.active_tab].configure(bg='#f0f0f0', fg='#000000', cursor='')

        return True

    def add(self, labels):
        if isinstance(labels, list):
            for label in labels:
                self._add_item(label)
        elif isinstance(labels, basestring):
            self._add_item(labels)
        else:
            raise TypeError('Should be a string or list of strings')

        return self

    def on_click(self, function):
        self.do_on_tab_click.append(function)
        return self

    def _add_item(self, label):
        tab = tkinter.Label(
            self.frame,
            text=label.upper(),
            bg=style['nav']['tab']['bg'],
            fg=style['nav']['tab']['color'],
            font=style['nav']['tab']['font'],
            padx=style['nav']['tab']['padx'],
            pady=style['nav']['tab']['pady'],
            cursor='hand2'
        )

        old_bg_color = tab['background']
        old_fg = tab['foreground']

        def handle_mouse_leave():
            if not tab['text'] == self.active_tab.upper():
                tab.configure(bg=old_bg_color, fg=old_fg)

        tab.bind("<Enter>", lambda e: tab.configure(bg='#f0f0f0', fg='#000000'))
        tab.bind("<Leave>", lambda e: handle_mouse_leave())
        tab.bind("<Button-1>", lambda e, txt=label: self.click_at(txt))
        tab.pack(side=tkinter.LEFT)

        self._tabs[label] = tab

        return True
