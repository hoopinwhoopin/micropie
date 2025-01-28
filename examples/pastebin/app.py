# -*- coding: utf-8 -*-
"""
A simple no frills pastebin using MicroPie, pickleDB, and highlight.js.
"""

from uuid import uuid4

from MicroPie import Server
from pickledb import PickleDB
from markupsafe import escape

db = PickleDB('pastes.db')

class Root(Server):

    async def index(self):
        # Check the HTTP method from the ASGI scope
        if self.scope["method"] == "POST":
            paste_content = self.body_params.get('paste_content', [''])[0]
            pid = str(uuid4())
            db.set(pid, escape(paste_content))
            db.save()
            return self.redirect(f'/paste/{pid}')
        return await self.render_template('index.html')

    async def paste(self, paste_id, delete=None):
        if delete == 'delete':
            db.remove(paste_id)
            db.save()
            return self.redirect('/')
        return await self.render_template(
            'paste.html',
            paste_id=paste_id,
            paste_content=db.get(paste_id)
        )


app = Root()
