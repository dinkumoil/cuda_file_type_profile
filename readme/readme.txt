FileTypeProfile plugin for CudaText.

Create profiles for files with certain filename extensions and apply the
settings automatically when opening a file.


This plugin is especially useful when coding Windows Batch scripts.

The Windows console still uses as character encoding schema the old DOS or OEM
code pages introduced back in the '80s by IBM. In nearly every country another
code page is used - and it's different from the default ANSI code page on the
same system.

If you write Batch scripts with an editor that uses the default ANSI code page
for your country, at its best your comments are displayed wrong when it comes to
other characters than the ones in the basic 7 bit ASCII range (character codes
from 32 to 127). But if you hard-code e.g. directory names into your script,
containing characters of your language with a character code beyond 127, you
will get a "Directory/File not found" error. That's the situation where this
plugin can help you.

You can create profiles for certain file types (distinguished by their file name
extension, e.g. *.cmd, *.bat) and define the code page and, as a bonus, the
end-of-line (EOL) format for all files that match one of the related file name
extension.

When you want to write a Batch script, AT FIRST create in Windows Explorer a new
file. Name it like you want and set its file name extension. Then open it in
CudaText. The plugin will automatically set the character encoding and the EOL-
format according to your configuration.

When CudaText runs the first time after plugin's installation, the plugin will
create a default config file in the CudatText settings directory. It contains
a template profile for Batch script files but lacks the values for all possible
settings. Set them, especially the "encoding" key according to your needs.

Possible values for the "encoding" setting you can find in the CudaText wiki,
see here: http://wiki.freepascal.org/CudaText#Encodings

There you can also find the possible values for the "eolFormat" setting, see
here: http://wiki.freepascal.org/CudaText#Line_ends



Author: Andreas Heim (dinkumoil, at github & sourceforge)
License: MIT
