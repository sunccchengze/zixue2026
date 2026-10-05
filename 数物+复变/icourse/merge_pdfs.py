import os, glob, re, unicodedata
from pypdf import PdfReader, PdfWriter

def safe(name, maxlen=80):
    name = unicodedata.normalize('NFKC', name or 'untitled')
    name = re.sub(r'[\\/:*?"<>|\r\n\t]+', '_', name).strip(' ._')
    return name[:maxlen] or 'untitled'

def merge_course(root):
    out_dir = os.path.join(root, '合并版')
    os.makedirs(out_dir, exist_ok=True)
    chapter_dirs = sorted(d for d in glob.glob(os.path.join(root, '*'))
                          if os.path.isdir(d) and os.path.basename(d) != '合并版')
    results = []
    for d in chapter_dirs:
        ch_name = os.path.basename(d)
        parts = sorted(glob.glob(os.path.join(d, '*.pdf')))
        if not parts:
            continue
        writer = PdfWriter()
        total_pages = 0
        used = []
        for p in parts:
            try:
                reader = PdfReader(p)
                n0 = len(reader.pages)
                for pg in reader.pages:
                    writer.add_page(pg)
                total_pages += n0
                used.append(os.path.basename(p))
            except Exception as e:
                print(f'  !! 跳过损坏文件 {p}: {e}')
        out_path = os.path.join(out_dir, safe(ch_name) + '.pdf')
        with open(out_path, 'wb') as fh:
            writer.write(fh)
        size = os.path.getsize(out_path)
        results.append((ch_name, len(used), len(parts), total_pages, size))
        print(f'{ch_name}: {len(used)}/{len(parts)} 份 -> {total_pages} 页, {size//1024} KB')
    return results

for root in ['/home/user/复变函数_课件_前五章', '/home/user/数学物理方程_课程课件']:
    print('====', root)
    merge_course(root)
