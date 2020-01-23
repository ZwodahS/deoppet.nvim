# ============================================================================
# FILE: deoppet.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import glob
import typing

from deoppet.parser import Parser, Snippet
from deoppet.mapping import Mapping
from deoppet.util import debug

from pynvim import Nvim


class Deoppet():

    def __init__(self, vim: Nvim) -> None:
        self._vim = vim
        if not self._vim.call('has', 'nvim-0.5.0'):
            return

        self._parser = Parser()
        self._mapping = Mapping(self._vim)
        self._options = self._vim.call('deoppet#custom#_get')['option']

        self._load_snippets()

        self._vim.call('deoppet#mapping#_init')
        self._vim.call('deoppet#handler#_init')

    def mapping(self, name: str) -> None:
        return self._mapping.mapping(name)

    def event(self, name: str) -> None:
        return self._mapping.clear()

    def _load_snippets(self) -> None:
        snippets: typing.Dict[str, Snippet] = {}
        filetype: str = self._vim.options['filetype']
        if not filetype:
            filetype = 'nothing'
        for dir in self._options['snippets_dirs']:
            for filename in glob.glob(
                    f'{dir}/{filetype}.snip') + glob.glob(f'{dir}/_.snip'):
                debug(self._vim, filename)
                with open(filename) as f:
                    snippets.update(self._parser.parse(f.read()))
        self._vim.current.buffer.vars['deoppet_snippets'] = snippets
