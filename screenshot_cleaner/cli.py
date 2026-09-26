from datetime import datetime
from pathlib import Path
import os
import re
import time
from .common import entry, parser, positive
SCREENSHOTS=True


def is_screenshot(path):
    return path.suffix.lower() in {'.png','.jpg','.jpeg','.webp'} and bool(re.match(r'^(screenshot|screen shot|スクリーンショット|スクリーン ショット)',path.stem,re.I))

def plan(root,mode):
    if not root.is_dir(): raise ValueError(f'フォルダがありません: {root}')
    result=[]
    for file in sorted(root.iterdir()):
        if not file.is_file() or file.is_symlink() or file.name.startswith('.'): continue
        if SCREENSHOTS and not is_screenshot(file): continue
        group=file.suffix.lower().lstrip('.') or 'no-extension'
        if mode=='date': group=datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d')
        elif mode=='month': group=datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m')
        target=root/group/file.name
        result.append((file,target))
    return result

def apply_moves(moves):
    # Atomic no-clobber linking on the same filesystem; never follows symlinks.
    for src,dst in moves:
        dst.parent.mkdir(parents=True,exist_ok=True)
        if dst.parent.is_symlink() or dst.exists(): raise ValueError(f'移動先が存在するかシンボリックリンクです: {dst}')
        os.link(src,dst,follow_symlinks=False)
        try: src.unlink()
        except OSError:
            dst.unlink(); raise

@entry
def main():
    p=parser('ファイルを整理。既定はプレビュー、--applyで移動。')
    p.add_argument('directory',nargs='?',default=str(Path.home()/('Desktop' if SCREENSHOTS else 'Downloads')))
    p.add_argument('--by',choices=['extension','date','month'],default='date' if SCREENSHOTS else 'extension')
    p.add_argument('--apply',action='store_true'); p.add_argument('--watch',type=positive,metavar='SECONDS')
    a=p.parse_args(); root=Path(a.directory).expanduser().resolve()
    if a.watch and not a.apply: p.error('--watchには--applyが必要です')
    while True:
        moves=plan(root,a.by)
        # Validate entire batch before any mutation.
        for src,dst in moves:
            if dst.exists() or dst.is_symlink() or dst.parent.is_symlink(): raise ValueError(f'移動先が既存です: {dst}')
        for src,dst in moves: print(f'{src.name} → {dst.relative_to(root)}',flush=True)
        if a.apply: apply_moves(moves)
        elif moves: print('プレビューのみ。移動するには --apply を付けてください。')
        if not a.watch: break
        time.sleep(a.watch)
