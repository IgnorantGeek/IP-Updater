import sys, argparse

interface = ""
cmd_string = "arp-scan --interface=enp6s0 --localnet"

def main():
    if len(sys.argv) < 2:
        print('Not enough arguments. Expected ')

    print(f'Arg count: {len(sys.argv)}')


def args():
    parser = argparse.ArgumentParser(description='TODO')

    parser.add_argument('interface', metavar='I', type=str, nargs=1, help='The network interface to pass to arp-scan')



if __name__ == "__main__":
    main()