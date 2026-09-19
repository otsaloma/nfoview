# AGENTS.md

## Environment

See `README.md` for which versions of Python, GTK, etc. we're currently
targeting. Regarding operating systems, we currently target only Linux
and *BSD, but try to avoid any OS-specific code. We want to keep any
existing Windows conditionals, but we don't want to worry about Windows
when adding new features. On Linux, we want to support all relevant
desktops and display servers, but GNOME + Wayland is whose conventions
we want to follow closest.

## GTK Documentation

Documentation for GTK and associated libraries is available as GIR files
under `/usr/share/gir-1.0`. Grep those for any symbols you need.

- `/usr/share/gir-1.0/Gdk-4.0.gir`
- `/usr/share/gir-1.0/Gio-2.0.gir`
- `/usr/share/gir-1.0/GLibUnix-2.0.gir`
- `/usr/share/gir-1.0/GObject-2.0.gir`
- `/usr/share/gir-1.0/Gtk-4.0.gir` etc.

Make sure you can access that GIR documentation; abort if not. Never
guess how the API works, always check from the documentation. Keep in
mind that we use Python and some of the documentation has been written
for C. You'll need adapt what you see there, for example:

- `GTK_ALIGN_CENTER` → `Gtk.Align.CENTER`
- `gtk_box_new(...)` → `Gtk.Box(...)`
- `gtk_widget_show(widget)` → `widget.show()`

## Validation, Testing

After making changes to Python code, always at minimum run `flake8 ...`
and `pytest ...` against all changed files. After making changes to
GtkBuilder `.ui` files, run `gtk4-builder-tool validate ...`. After
bigger changes, or if you suspect your changes affect other modules, use
`make check` and `make test` to run the full validation and test suites.

## Running the GUI

You can run the GUI as `timeout --signal=TERM 5 bin/nfoview README.md`
so it self-terminates (exit 124) instead of blocking; the console output
is then captured for inspection.

To see all warnings, set `G_ENABLE_DIAGNOSTIC=1` (forces GTK to emit
deprecation warnings) and read stderr (`2>&1`). GTK/GLib warnings go
through the GLib log system, not Python `warnings`, so `pytest` needs
`-s` to show them. Use `G_DEBUG=fatal-warnings` to turn a warning into a
fatal error (with traceback) when tracking down its source.

Note that some previous version of nfoview might be installed under a
system directory, such as `/usr/local`. When running a standalone
verification script, make sure your `PYTHONPATH` or `sys.path` points to
the source repo. Check `nfoview.__file__` in the script if unsure.

## Screenshots

To screenshot the app, run a standalone script that creates
`nfoview.Application(paths)`, then in a `GLib.timeout_add` callback
(~1500 ms, inside a `GLib.MainLoop`) render the `window =
app.get_active_window()` to PNG:

```python
paintable = Gtk.WidgetPaintable(widget=window)
snapshot = Gtk.Snapshot()
paintable.snapshot(snapshot, paintable.get_intrinsic_width(), paintable.get_intrinsic_height())
texture = window.get_native().get_renderer().render_texture(snapshot.to_node())
texture.save_to_png(path)
```

This captures the window content regardless of the Wayland compositor.
The same recipe works for dialogs (snapshot the dialog widget instead),
such as built via the dialog test classes' `setup_method`.
