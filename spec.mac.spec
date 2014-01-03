a = Analysis(['portablizer.pyqt5.py'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Portablizer',
          debug=False,
          strip=None,
          upx=True,
          console=True)
bundle = BUNDLE(exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                info_plist={
                  'NSHighResolutionCapable': 'True',
                  'LSBackgroundOnly': '0'
                },
                version='0.0.0',
                name='Portablizer.app')
