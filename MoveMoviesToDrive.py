import os
from tqdm import tqdm
import shutil


class CTError(Exception):
    def __init__(self, errors):
        self.errors = errors


try:
    O_BINARY = os.O_BINARY
except:
    O_BINARY = 0
READ_FLAGS = os.O_RDONLY | O_BINARY
WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | O_BINARY
BUFFER_SIZE = 128*1024


def copyfile(src, dst):
    try:
        # Check if file already exists in destination with the same size
        if os.path.exists(dst) and os.path.getsize(src) == os.path.getsize(dst):
            return

        fin = os.open(src, READ_FLAGS)
        stat = os.fstat(fin)
        fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
        total_size = os.path.getsize(src)
        progress_bar = tqdm(total=total_size, unit='B',
                            unit_scale=True, desc=os.path.basename(src))
        for x in iter(lambda: os.read(fin, BUFFER_SIZE), b""):
            os.write(fout, x)
            progress_bar.update(len(x))
        shutil.copystat(src, dst)
        progress_bar.close()
    finally:
        try:
            os.close(fin)
        except:
            pass
        try:
            os.close(fout)
        except:
            pass


def copytree(src, dst, symlinks=False, ignore=[]):
    names = os.listdir(src)

    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignore:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                copyfile(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except CTError as err:
            errors.extend(err.errors)
    if errors:
        raise CTError(errors)


src_directory = 'E:\\Media\\Anime'
dst_directory = 'D:\\Media\\Anime'
copytree(src_directory, dst_directory, symlinks=False, ignore=[])

src_directory = 'E:\\Media\\TV Shows'
dst_directory = 'D:\\Media\\TV'
copytree(src_directory, dst_directory, symlinks=False, ignore=[])

src_directory = 'E:\\Media\\Movies'
dst_directory = 'D:\\Media\\Movies'
copytree(src_directory, dst_directory, symlinks=False, ignore=[])
