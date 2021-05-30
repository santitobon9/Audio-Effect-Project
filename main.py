import argparse

def main():


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Audio Effects',
                                    description='Simple Audio Effects'
                                    ' program for sound and music',
                                    allow_abbrev=False)
    parser.add_argument('-r', '--record',
                        type=str,
                        default='temp_file')
    parser.add_argument('-f', '--file',
                        type=str)
    parser.add_argument('-af', '--apply_filter',
                        type=str)
    parser.add_argument('-p', '--play',
                        type=str)

    args = parser.parse_args()

    main(args)

    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye!')
