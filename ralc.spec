# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['ralc.py'],
             pathex=[],
             binaries=[],
             datas=[('icons\\spider.ico','icons'),
						('help\\index.html','help'),
						('help\\style.css','help'),
						('help\\files\\hamlog1.jpg','help\\files'),
						('help\\files\\hamlog2.jpg','help\\files'),
						('help\\files\\ralc-settings-1.jpg','help\\files'),
						('help\\files\\ralc-settings-2.jpg','help\\files'),
						('help\\files\\ralc-settings-3.jpg','help\\files'),
						('help\\files\\ralc-settings-4.jpg','help\\files'),
						('help\\files\\ralc-settings-5.jpg','help\\files'),
						('help\\files\\ralc-spots-1.jpg','help\\files')
						],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
			 
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='ralc',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
		  icon='icons\\spider.ico')
