# cmd_line.py
from lstm_query_completion import load_models, \
    query_completions


def main():
    import sys
    models = load_models()
    while True:
        query = input('Please enter a query (q to quit):\n')
        if query == 'q':
            print('Exiting program.')
            sys.exit(0)
        completions = query_completions(models, query, 3)
        if completions is None:
            continue
        print_completions(query, completions)


def print_completions(query, completions):
    print(f"completions for '{query}':")
    for cpl, prob in sorted(completions.items(), key=lambda e: -e[1]):
        print(f'\t{cpl} ({prob*100:.2f}%)')


if __name__ == '__main__':
    main()
