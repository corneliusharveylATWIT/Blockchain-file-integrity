import json, hashlib, time, os
from dataclasses import dataclass, asdict

@dataclass
class Block:
    index: int
    timestamp: float
    filename: str
    filehash: str
    prev_hash: str

    def to_json(self):
        return json.dumps(asdict(self), sort_keys=True)

    def hash(self):
        return hashlib.sha256(self.to_json().encode()).hexdigest()

class Blockchain:
    @staticmethod
    def init_chain(path='chain.jsonl'):
        if os.path.exists(path):
            print(f'Chain already exists at {path}')
            return
        genesis = Block(index=0, timestamp=time.time(), filename='__genesis__', filehash='', prev_hash='0'*64)
        with open(path,'w') as f:
            f.write(genesis.to_json() + '\n')
        print('Initialized chain at', path)

    @staticmethod
    def append_block(path, filename, filehash):
        # read last block
        last = None
        if os.path.exists(path):
            with open(path,'r') as f:
                for line in f:
                    if line.strip():
                        last = json.loads(line)
        if last is None:
            prev_hash = '0'*64
            index = 0
        else:
            prev_block_json = json.dumps(last, sort_keys=True)
            prev_hash = hashlib.sha256(prev_block_json.encode()).hexdigest()
            index = last.get('index',0) + 1
        blk = Block(index=index, timestamp=time.time(), filename=filename, filehash=filehash, prev_hash=prev_hash)
        with open(path,'a') as f:
            f.write(blk.to_json()+'\n')
        print(f'Appended block #{index} for {filename} to {path}')

    @staticmethod
    def validate_chain(path):
        if not os.path.exists(path):
            print('Chain file not found:', path)
            return False
        prev_hash = '0'*64
        idx = 0
        with open(path,'r') as f:
            for line in f:
                if not line.strip(): continue
                obj = json.loads(line)
                # recompute prev_hash check
                if obj.get('prev_hash') != prev_hash and idx!=0:
                    print(f'Invalid prev_hash at index {idx}: expected {prev_hash}, got {obj.get("prev_hash")}')
                    return False
                # recompute this block's hash to become prev_hash for next
                block_json = json.dumps(obj, sort_keys=True)
                prev_hash = hashlib.sha256(block_json.encode()).hexdigest()
                idx += 1
        print('Chain validated: {} blocks'.format(idx))
        return True

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python blockchain.py validate|init <chainfile>')
        sys.exit(1)
    cmd = sys.argv[1]
    path = sys.argv[2] if len(sys.argv)>2 else 'chain.jsonl'
    if cmd == 'init':
        Blockchain.init_chain(path)
    elif cmd == 'validate':
        Blockchain.validate_chain(path)
    else:
        print('Unknown cmd', cmd)
