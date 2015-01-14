""" HTML5 runtime based on a common browser

Opens browser via webbrowser module.
"""

import webbrowser
import logging

from .common import HTML5Runtime


BROWSER_MAP = {'chrome': ['google-chrome', 'chrome', 
                          'chromium-browser', 'chromium'],
               'chromium': ['chromium-browser', 'chromium'],
               'default': [],
               }


class BrowserRuntime(HTML5Runtime):
    
    def _launch(self):
        
        # Get url and browser type
        url = self._kwargs['url']
        type = self._kwargs.get('browsertype', '')
        
        # Get alternative types
        types = BROWSER_MAP.get(type, [type])
        types = [t for t in types if t]
        
        # Try to open all possibilities
        errors = []
        for t in types:
            try:
                b = webbrowser.get(t)
            except webbrowser.Error as err:
                errors.append(str(err))
            else:
                b.open(url)
                return
        
        # If that did not work, maybe we should try harder
        # In particular on Windows, the exes may simply not be on the path
        if type == 'firefox':
            from .xul import get_firefox_exe
            exe = get_firefox_exe() or 'google-chrome'
            self._start_subprocess([exe, url])
            self._proc = None  # Prevent closing
            return
        elif type == 'chrome':
            from .chromeapp import get_chrome_exe
            exe = get_chrome_exe() or 'google-chrome'
            self._start_subprocess([exe, url])
            self._proc = None  # Prevent closing
            return
        elif type == 'chromium':
            from .chromeapp import get_chromium_exe
            exe = get_chromium_exe() or 'chromium-browser'
            self._start_subprocess([exe, url])
            self._proc = None  # Prevent closing
            return
        
        if errors:
            logging.warn('Given browser %r not valid/available;\n'
                         'Falling back to the default browser.' % type)
        
        # Run default
        webbrowser.open(url)
