
## Development Tips

### Inspect GTK+3 Themes

The inspector allows you to figure out the classes and properties used to make
up the theme. First, make sure you have the development files installed:

    sudo apt install libgtk-3-dev

Set this environment variable and launch the application:

    export GTK_DEBUG=interactive
    pluma

[More information on the Ubuntu MATE Community.](https://ubuntu-mate.community/t/20150)


### Test with the Widget Factory

The Widget Factory is a basic application with generic controls, useful for testing
the theme and icons. This is provided in the GTK+3 examples package:

    sudo apt install gtk-3-examples

To launch:

    gtk3-widget-factory

(You can edit your MATE menu to show this application, it's under "Programming")

