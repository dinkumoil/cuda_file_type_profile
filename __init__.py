import os
import cudatext_cmd
from cudatext import *


# full path to INI file
fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_file_type_profile.ini')

# names of keys in INI file
key_file_ext_list = 'FileExts'
key_encoding      = 'Encoding'
key_eol_format    = 'EolFormat'


# debug output header
dbg_header = '(cuda_file_type_profile) '


# data model of INI file
ini_file = {}

# PROCESSED FILES list
documents = []


# mapping of encoding names to commands for encoding switching
enc_map = {
    'utf8'        : cudatext_cmd.cmd_Encoding_utf8nobom_Reload,
    'utf8_bom'    : cudatext_cmd.cmd_Encoding_utf8bom_Reload,
    'utf16le'     : cudatext_cmd.cmd_Encoding_utf16le_Reload,
    'utf16le_bom' : cudatext_cmd.cmd_Encoding_utf16le_Reload,
    'utf16be'     : cudatext_cmd.cmd_Encoding_utf16be_Reload,
    'utf16be_bom' : cudatext_cmd.cmd_Encoding_utf16be_Reload,
    'utf32le'     : cudatext_cmd.cmd_Encoding_utf32le_Reload,
    'utf32le_bom' : cudatext_cmd.cmd_Encoding_utf32le_Reload,
    'utf32be'     : cudatext_cmd.cmd_Encoding_utf32be_Reload,
    'utf32be_bom' : cudatext_cmd.cmd_Encoding_utf32be_Reload,
    'cp1250'      : cudatext_cmd.cmd_Encoding_cp1250_Reload,
    'cp1251'      : cudatext_cmd.cmd_Encoding_cp1251_Reload,
    'cp1252'      : cudatext_cmd.cmd_Encoding_cp1252_Reload,
    'cp1253'      : cudatext_cmd.cmd_Encoding_cp1253_Reload,
    'cp1254'      : cudatext_cmd.cmd_Encoding_cp1254_Reload,
    'cp1255'      : cudatext_cmd.cmd_Encoding_cp1255_Reload,
    'cp1256'      : cudatext_cmd.cmd_Encoding_cp1256_Reload,
    'cp1257'      : cudatext_cmd.cmd_Encoding_cp1257_Reload,
    'cp1258'      : cudatext_cmd.cmd_Encoding_cp1258_Reload,
    'cp437'       : cudatext_cmd.cmd_Encoding_cp437_Reload,
    'cp850'       : cudatext_cmd.cmd_Encoding_cp850_Reload,
    'cp852'       : cudatext_cmd.cmd_Encoding_cp852_Reload,
    'cp866'       : cudatext_cmd.cmd_Encoding_cp866_Reload,
    'cp874'       : cudatext_cmd.cmd_Encoding_cp874_Reload,
    'cp932'       : cudatext_cmd.cmd_Encoding_cp932_Reload,
    'cp936'       : cudatext_cmd.cmd_Encoding_cp936_Reload,
    'cp949'       : cudatext_cmd.cmd_Encoding_cp949_Reload,
    'cp950'       : cudatext_cmd.cmd_Encoding_cp950_Reload,
    'iso88591'    : cudatext_cmd.cmd_Encoding_iso1_Reload,
    'iso88592'    : cudatext_cmd.cmd_Encoding_iso2_Reload,
    'iso885915'   : cudatext_cmd.cmd_Encoding_iso15_Reload,
    'mac'         : cudatext_cmd.cmd_Encoding_mac_Reload
}


# mapping of EOL format names to commands for EOL format switching
eol_map = {
    'crlf' : cudatext_cmd.cmd_LineEndWin,
    'lf'   : cudatext_cmd.cmd_LineEndUnix,
    'cr'   : cudatext_cmd.cmd_LineEndMac
}




class Command:

    def do_init(self):
        global fn_config
        global ini_file
        global key_file_ext_list
        global key_encoding
        global key_eol_format

        # if INI file doesn't exist create it with standard content
        if not os.path.isfile(fn_config):
            ini_write(fn_config, 'Header', 'Version', '1.0')
            ini_write(fn_config, 'BatchScript', key_file_ext_list, '.cmd;.bat;.nt')
            ini_write(fn_config, 'BatchScript', key_encoding, '')
            ini_write(fn_config, 'ShellScript', key_file_ext_list, '.sh')
            ini_write(fn_config, 'ShellScript', key_eol_format, 'lf')

        # iterate over all sections of the INI file
        for ini_section_name in ini_proc(INI_GET_SECTIONS, fn_config):
            # create a dictionary for every INI file section and a list
            # for all filename extensions in the section
            cur_section    = {}
            file_name_exts = []

            # iterate over all keys of current section
            for ini_key_name in ini_proc(INI_GET_KEYS, fn_config, ini_section_name):
                # if key is a filename extension store value in list
                if ini_key_name.lower() == key_file_ext_list.lower():
                    file_name_exts = ini_read(fn_config, ini_section_name, ini_key_name, '').lower().split(';')

                # if key is an encoding store it in dictionary
                elif ini_key_name.lower() == key_encoding.lower():
                    cur_section[key_encoding] = ini_read(fn_config, ini_section_name, ini_key_name, '').lower()

                # if key is an EOL format store it in dictionary
                elif ini_key_name.lower() == key_eol_format.lower():
                    cur_section[key_eol_format] = ini_read(fn_config, ini_section_name, ini_key_name, '').lower()

            # if we have a list of filename extensions
            # store section's dictionary in main dictionary of INI file
            if len(file_name_exts) > 0:
                cur_section[key_file_ext_list] = file_name_exts
                ini_file[ini_section_name] = cur_section


    def do_config(self):
        # load INI file and set flag that it's in edit mode
        global fn_config

        file_open(fn_config)


    def do_apply_profile_settings(self, editor, file_name_full, file_extension):
        global ini_file
        global documents
        global key_file_ext
        global key_file_ext_list
        global key_encoding
        global key_eol_format

        settings_applied = False

        # if the current document is NOT part of a saved session or file history
        # and also hasn't been processed yet ...
        if (not editor.get_prop(PROP_IN_SESSION, file_name_full) and
            not editor.get_prop(PROP_IN_HISTORY, file_name_full) and
            file_name_full not in documents):
            # ...iterate over all INI file sections
            for sectionName, section_items in ini_file.items():
                # if the current section contains a list of file extensions
                # and the file's extension is part of that list ...
                if key_file_ext_list in section_items and file_extension.lower() in section_items[key_file_ext_list]:
                    # ...check if section has valid key for character encoding
                    if key_encoding in section_items and section_items[key_encoding].lower() in enc_map:
                        # switch character encoding, remember that file has been
                        # processed in PROCESSED FILES list
                        documents.append(file_name_full)
                        editor.cmd(enc_map[section_items[key_encoding].lower()])
                        settings_applied = True

                    # ...check if section has valid key for EOL format
                    if key_eol_format in section_items and section_items[key_eol_format].lower() in eol_map:
                        # switch EOL format, remember that file has been processed in
                        # PROCESSED FILES list
                        documents.append(file_name_full)
                        editor.cmd(eol_map[section_items[key_eol_format].lower()])
                        settings_applied = True

                    # if file has been processed, return CHANGED to caller
                    if settings_applied:
                        return True
                    # if not, there are no valid settings for the file's type
                    # thus stop processing of INI file and return NOTHING
                    # CHANGED to caller
                    else:
                        return False

        # return NOTHING CHANGED to caller
        return False


    def do_save_file(self, editor):
        # if saved file is INI file discard its data model and reload it
        global fn_config
        global ini_file

        if editor.get_filename('*').lower() == fn_config.lower():
            ini_file = {}
            self.do_init()
            # print(dbg_header + 'Settings file has been reloaded')


    def apply_profile_settings(self, editor, caller):
        # retrieve full filename and extension (including dot)
        file_name_full = editor.get_filename('*')
        file_name, file_extension = os.path.splitext(file_name_full)

        # check if character encoding has been changed
        # and output log message to console
        if self.do_apply_profile_settings(editor, file_name_full, file_extension):
            # print(dbg_header + 'Method ' + caller + ' applied settings on file: ' + file_name_full)
            pass


    def unregister_file(self, editor, caller):
        global documents

        # retrieve full filename
        file_name_full = editor.get_filename('*')

        # check if filename is member of PROCESSED FILES list
        # if yes, remove it from list and output log message to console
        if file_name_full in documents:
            documents.remove(file_name_full)
            # print(dbg_header + 'Method ' + caller + ' unregistered file: ' + file_name_full)


    def __init__(self):
        self.do_init()


    def config(self):
        self.do_config()


    def on_open(self, ed_self):
        # change character encoding if necessary
        self.apply_profile_settings(ed_self, 'on_open')


    def on_save(self, ed_self):
        # if INI file is in editmode reload it and build up its data model
        self.do_save_file(ed_self)


    def on_close(self, ed_self):
        # remove file from PROCESSED FILES list
        self.unregister_file(ed_self, 'on_close')
