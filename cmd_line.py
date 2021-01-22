# cmd_line.py
from lstm_query_completion import load_nextcharlstm_objs, \
    query_completions


def main():
    import sys
    models = load_nextcharlstm_objs()
    while True:
        query = input('Please enter a query (q to quit):\n')
        if query == 'q':
            print('Exiting program.')
            sys.exit(0)
        completions, lstm_probs = query_completions(models, query, 3)
        if completions is None:
            continue
        print_completions(query, completions, lstm_probs)


def print_completions(query, completions, lstm_probs):
    print(f"completions for '{query}':")
    for cpl, prob in sorted(completions.items(), key=lambda e: -e[1]):
        cpl_only = cpl[len(query):]
        print(f"\t'{cpl}'  |  Query completion likelihood P('{cpl_only}'|'{query}') = {prob*100:.2f}%")
        for c, lstm_cpl, lstm_prob in sorted(lstm_probs[cpl], key=lambda e: len(e[1])):
            print(f"\t\t\t    Using n = {len(lstm_cpl)} lstm model, P('{c}'|'{lstm_cpl}') = {lstm_prob*100:.2f}% ")


if __name__ == '__main__':
    main()
