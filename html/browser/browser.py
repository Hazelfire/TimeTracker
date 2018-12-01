from gi.repository import Gtk, WebKit2  # gir1.2-webkit2-3.0
from os.path import abspath, dirname, join
import sys

WHERE_AM_I = abspath(dirname(__file__))


local_uri = 'webbrowser://'
initial_html = '''\
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>WebView Recipe</title>
</head>
<body>
<p>Some links:</a>
<ul>
    <li><a href="https://www.google.com/">Google</a></li>
    <li><a href="http://www.gtk.org/">Gtk+</a></li>
    <li><a href="https://glade.gnome.org/">Glade</a></li>
    <li><a href="http://www.python.org/">Python</a></li>
    <li><a href="file:///etc/hosts">Local <tt>/etc/hosts</tt> file</a></li>
</ul>
</body>
</html>
'''


class WebBrowser(object):
    """
    Simple WebBrowser class.
    Uses WebKit introspected bindings for Python:
    http://webkitgtk.org/reference/webkit2gtk/stable/
    """

    def __init__(self):
        """
        Build GUI
        """
        # Build GUI from Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(join(WHERE_AM_I, 'webbrowser.ui'))

        # Get objects
        go = self.builder.get_object
        self.window = go('window')

        # Create WebView
        self.webview = WebKit2.WebView()
        self.window.add_with_viewport(self.webview)

        # Connect signals
        self.builder.connect_signals(self)
        self.webview.connect('load-changed', self.load_changed_cb)
        self.window.connect('delete-event', Gtk.main_quit)

        # Everything is ready
        self.load_uri(sys.argv[1])
        self.window.show_all()

    def entry_cb(self, widget, user_data=None):
        """
        Callback when Enter is pressed in URL entry.
        """
        self.load_uri(self.entry.get_text())

    def load_changed_cb(self, webview, event, user_data=None):
        """
        Callback for when the load operation in webview changes.
        """
        ev = str(event)
        if 'WEBKIT_LOAD_COMMITTED' in ev:
            self.entry.set_text(self.webview.get_uri())

    def load_uri(self, uri):
        """
        Load an URI on the browser.
        """
        self.entry.set_text(uri)
        if uri.startswith(local_uri):
            section = uri[len(local_uri):]
            if section == 'home':
                self.webview.load_html(initial_html, local_uri)
                return
        self.webview.load_uri(uri)
        return


if __name__ == '__main__':
    gui = WebBrowser()
Gtk.main()
