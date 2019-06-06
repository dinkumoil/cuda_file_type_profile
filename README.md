# FileTypeProfile plugin for CudaText

**Create profiles for files with certain filename extensions and apply the
settings automatically when opening a file.**

**This plugin is especially useful when coding Windows Batch scripts or if you
have to write, for whatever reason, e.g. Linux shell scripts on a Windows
machine.**


The Windows console still uses as character encoding schema the old DOS or OEM
code pages introduced back in the '80s by IBM. In nearly every country another
code page is used - and it's different from the default ANSI code page on the
same system.

If you write Batch scripts with an editor that uses the default ANSI code page
for your country, at its best your comments are displayed wrong when it comes to
other characters than the ones in the basic 7 bit ASCII range (character codes
from 32 to 127). But if you hard-code e.g. directory names into your script,
containing characters of your language with a character code beyond 127, you
will get a "Directory/File not found" error.

If you have to write Linux shell scripts on a Windows machine and forget to set
the end-of-line format to the Unix/Linux style you will produce a script file
which can not be executed.

These are the situations this plugin can help you.

# Features

You can create profiles for certain file types (distinguished by their filename
extension, e.g. _*.cmd_, _*.bat_) and define the code page and/or the end-of-line
(EOL) format that should be set when a file matching a profile has been loaded.

When you want to start writing a script, **at first** create in Windows Explorer a
new file. Name it like you want and set its filename extension. Then open it in
CudaText. The plugin will automatically set the character encoding and/or the
EOL format according to your configuration.

When CudaText runs the first time after plugin's installation, the plugin will
create a default config file in the CudatText settings directory. It contains
a template profile for Batch script files but lacks the values for all possible
settings. Set them, especially the _Encoding_ key, according to your needs.

If you want to change the plugin's config file, navigate to
`(menu) Options -> Settings - plugins -> File type profile -> Config`. The
config file will be opened. Edit its content and save it. In that moment the
plugin will automatically reload the file and update its configuration. **Please
note:** Only newly opened files will be affected by the updated configuration,
already opened ones will not.

Possible values for the _Encoding_ setting you can find in the CudaText wiki,
see here: http://wiki.freepascal.org/CudaText#Encodings

There you also can find the possible values for the _EolFormat_ setting, see
here: http://wiki.freepascal.org/CudaText#Line_ends


Author: Andreas Heim (dinkumoil, at github & sourceforge)

License: MIT
