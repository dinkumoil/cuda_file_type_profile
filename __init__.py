import os
from cudatext import *


# full path to INI file
fnConfig = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_filetypeprofile.ini')


# names of keys in INI file
keyFileExt     = 'fileExt'
keyFileExtList = 'fileExts'
keyEncoding    = 'encoding'
keyEolFormat   = 'eolFormat'


# data model of INI file
iniFile = {}

# PROCESSED FILES list
documents = []

# edit mode flag of INI file
reloadSettings = False



class Command:

    def do_init(self):
        global fnConfig
        global iniFile
        global keyFileExt
        global keyFileExtList
        global keyEncoding
        global keyEolFormat

        # if settings file doesn't exist create it with standard content
        if not os.path.isfile(fnConfig):
            ini_write(fnConfig, 'Header', 'Version', '1.0')
            ini_write(fnConfig, 'BatchScript', keyFileExt + str(1), '.bat')
            ini_write(fnConfig, 'BatchScript', keyFileExt + str(2), '.cmd')
            ini_write(fnConfig, 'BatchScript', keyFileExt + str(3), '.nt')
            ini_write(fnConfig, 'BatchScript', keyEncoding, '')
            ini_write(fnConfig, 'BatchScript', keyEolFormat, '')

        # iterate over all sections of the settings INI file
        for iniSectionName in ini_proc(INI_GET_SECTIONS, fnConfig):
            # create a dictionary for every INI file section and a list
            # for all filename extensions in the section
            curSection   = {}
            filenameExts = []

            # iterate over all keys of current section
            for iniKeyName in ini_proc(INI_GET_KEYS, fnConfig, iniSectionName):
                # if key is a filename extension store value in list
                if iniKeyName.lower().startswith(keyFileExt.lower()):
                    filenameExts.append(ini_read(fnConfig, iniSectionName, iniKeyName, '').lower())

                # if key is an encoding store it in dictionary
                elif iniKeyName.lower() == keyEncoding.lower():
                    curSection[keyEncoding] = ini_read(fnConfig, iniSectionName, iniKeyName, '').lower()

                # if key is an EOL format store it in dictionary
                elif iniKeyName.lower() == keyEolFormat.lower():
                    curSection[keyEolFormat] = ini_read(fnConfig, iniSectionName, iniKeyName, '').lower()

            # if we have a list of filename extensions
            # store section's dictionary in main dictionary of INI file
            if len(filenameExts) > 0:
                curSection[keyFileExtList] = filenameExts
                iniFile[iniSectionName] = curSection


    def do_config(self):
        # load settings file and set flag that it's in edit mode
        global fnConfig
        global reloadSettings

        file_open(fnConfig)
        reloadSettings = True


    def do_ApplyProfileSettings(self, editor, fileNameFull, fileExtension):
        global iniFile
        global documents
        global keyFileExt
        global keyFileExtList
        global keyEncoding
        global keyEolFormat

        settingsApplied = False

        # if the current document hasn't been processed yet ...
        if fileNameFull not in documents:
            # ...iterate over all INI file sections
            for sectionName, sectionItems in iniFile.items():
                # if the current section contains a list of file extensions
                # and the file's extension is part of that list ...
                if keyFileExtList in sectionItems and fileExtension.lower() in sectionItems[keyFileExtList]:
                    # ...check if section has valid key for character encoding
                    if keyEncoding in sectionItems and sectionItems[keyEncoding] != '':
                        # switch character encoding
                        editor.set_prop(PROP_ENC, sectionItems[keyEncoding])
                        settingsApplied = True

                    # ...check if section has valid key for EOL format
                    if keyEolFormat in sectionItems and sectionItems[keyEolFormat] != '':
                        # switch EOL format
                        editor.set_prop(PROP_NEWLINE, sectionItems[keyEolFormat])
                        settingsApplied = True

                    # if settings have been applied, remember that file has been
                    # processed in PROCESSED FILES list and return CHANGED to caller
                    if settingsApplied:
                        documents.append(fileNameFull)
                        return True

        # return NOTHING CHANGED to caller
        return False


    def do_SaveFile(self, editor):
        global fnConfig
        global iniFile
        global reloadSettings

        if reloadSettings and editor.get_filename('*').lower() == fnConfig.lower():
            iniFile = {}
            self.do_init()
            print('(FileTypeProfile) Settings file has been reloaded')


    def do_PreCloseFile(self, editor):
        global fnConfig
        global reloadSettings

        if reloadSettings and editor.get_filename('*').lower() == fnConfig.lower():
            reloadSettings = False


    def ApplyProfileSettings(self, editor, caller):
        # retrieve full filename and extension (including dot)
        fileNameFull = editor.get_filename('*')
        fileName, fileExtension = os.path.splitext(fileNameFull)

        # check if character encoding has been changed
        # and output log message to console
        if self.do_ApplyProfileSettings(editor, fileNameFull, fileExtension):
            print('(FileTypeProfile) ' + caller + " applied settings: " + fileNameFull)


    def UnregisterFile(self, editor, caller):
        global documents

        # retrieve full filename
        fileNameFull = editor.get_filename('*')

        # check if filename is member of PROCESSED FILES list
        # if yes, remove it from list and output log message to console
        if fileNameFull in documents:
            documents.remove(fileNameFull)
            print('(FileTypeProfile) ' + caller + " unregistered file: " + fileNameFull)


    def __init__(self):
        self.do_init()


    def config(self):
        self.do_config()


    def run(self):
        pass


    def on_open(self, ed_self):
        # change character encoding if necessary
        self.ApplyProfileSettings(ed_self, 'FileOpened')


    def on_save(self, ed_self):
        # if settings file is in editmode reload it and build up its data model
        self.do_SaveFile(ed_self)


    def on_close_pre(self, ed_self):
        # reset edit mode flag of settings file
        self.do_PreCloseFile(ed_self)


    def on_close(self, ed_self):
        # remove file from PROCESSED FILES list
        self.UnregisterFile(ed_self, 'FileClosed')
