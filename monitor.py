import sys, hashlib, os
from blockchain import Blockchain

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def add_file(chainpath, filepath):
    if not os.path.exists(filepath):
        print('file not found', filepath)
        return
    filehash = sha256_of_file(filepath)
    Blockchain.append_block(chainpath, os.path.basename(filepath), filehash)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python monitor.py add <file> [chainfile]')
        sys.exit(1)
    op = sys.argv[1]
    if op == 'add':
        fp = sys.argv[2]
        chain = sys.argv[3] if len(sys.argv) > 3 else 'chain.jsonl'
        add_file(chain, fp)
    else:
        print('Unknown op', op)
