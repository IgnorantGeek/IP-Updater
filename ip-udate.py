import sys, argparse, subprocess, re, json, os, pathlib, copy

interface = ""
cmd = ['sudo', 'arp-scan', '--localnet']
hitlist = {}
update = {}
write  = {}

# --------- MAIN --------------------------------------------------------------
def main():
    arg = args()

    cfg_d = cfg()

    for key, value in cfg_d.items():
        if key == 'hitlist':
            if type(value) is not dict:
                print('INVALID HITLIST TYPE')
                return 1
            
            hitlist = value
        
        if key == 'update':
            if type(value) is not dict:
                print('INVALID UPDATE TYPE')
                return 1
            
            update = value

    cmd.append(f"--interface={arg['interface']}")

    if arg['verbose']: print(f'RAW CMD: {cmd}')

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out = result.stdout.decode('UTF-8')
    err = result.stderr.decode('UTF-8')

    if err:
        print('Theres been a problem\n')
        print(err)
        return 1

    out_lines = out.split('\n')[2:]  # Get everything but the first 2 lines (garbage data)

    hit = False
    for line in out_lines:
        entry = line.split('\t')

        if len(entry) < 3: continue

        name = entry[2].lower()

        for key in hitlist.keys():
            if key in name:
                hit = True

                hitlist[key] = entry[0]

                break
    
    if not hit:
        print('No matches found.')
        return 2
    
    # Need a deep copy
    write = copy.deepcopy(update)
    
    # Now we know there is at least 1 hit    
    for path, ptrn in update.items():
        found = False
        for key, value in hitlist.items():
            if not value: continue

            if type(ptrn) == list:
                for i in range(0, len(ptrn)):
                    if f'&{key}' in ptrn[i]:
                        out = re.sub(f'&{key}', value, ptrn[i])
                        write[path][i] = out

                        update_str = re.sub(f'&{key}', r'\\d{1,3}.\\d{1,3}.\\d{1,3}.\\d{1,3}', ptrn[i])
                        ptrn[i] = update_str
                        found = True

                continue

            if f'&{key}' in ptrn:
                out = re.sub(f'&{key}', value, ptrn)
                write[path] = out

                update_str = re.sub(f'&{key}', r"\\d{1,3}.\\d{1,3}.\\d{1,3}.\\d{1,3}", ptrn)
                update[path] = update_str
                found = True
        
        if not found:
            update[path] = None
            write[path] = None
    
    # print(write)
    # print(update)

    # Now iterate through update and update all files who's value is not none
    # Inform user if the file does not exist and prompt to continue
    for path, ptrn in update.items():
        if not ptrn: continue

        if not os.path.isfile(path):
            print(f"The file '{path} could not be found.")
            answer = input("Would you like to continue? Enter 'n' to exit, or press Enter to continue\n")

            if answer.lower().startswith('n'):
                print('Aborting...')
                return 1
            else: continue

        print(f'Reading file {path}')
        f = open(path, 'r')
        file_str = f.read()
        f.close()

        if type(ptrn) == list:
            for i in range(0, len(ptrn)):
                match = re.search(ptrn[i], file_str)
                if match:
                    print(f'MATCH FOUND: {match}')
                    file_str = re.sub(ptrn[i], write[path][i], file_str)
        
        else:
            match = re.search(ptrn, file_str)
            if match:
                print(f'MATCH FOUND: {match}')
                file_str = re.sub(ptrn, write[path], file_str)
        
        # Rewrite file
        f = open(path, 'w')
        f.write(file_str)
        f.close()

    # Out
    return 0



# --------- FUNCTIONS ---------------------------------------------------------
def get_dir():
    return os.path.abspath(__file__)
    
def cfg():
    script_path = pathlib.Path(get_dir()).parent
    cfg_path = str(script_path / 'config.json')

    if not os.path.isfile(cfg_path):
        return None
    
    f = open(cfg_path, 'r')

    return json.loads(f.read())


def args():
    parser = argparse.ArgumentParser(description='TODO')

    parser.add_argument('interface', metavar='I', type=str, help='The network interface to pass to arp-scan')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Enables extra logging messages')

    return vars(parser.parse_args())

# --------- ENTRY -------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())