from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all data files from rich
datas = collect_data_files('rich')

# Collect all submodules including _unicode_data
hiddenimports = collect_submodules('rich')
