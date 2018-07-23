from random import randint
from sys import argv

default_choices = 4
default_answers = 20
default_trials = 100000

def getNum(i, default):
    try:
        return int(argv[i])
    except:
        return default

def main():
    global default_trials

    try:
        if len(argv) > 4:
            raise

        num_choices = getNum(1, default_choices)
        num_answers = getNum(2, default_answers)
        num_trials = getNum(3, default_trials)

    except:
        print (
          'Usages:\n'+
          '  python main.py\n'+
          '  python main.py num_choices\n'+
          '  python main.py num_choices num_answers\n'+
          '  python main.py num_choices num_answers num_trials\n\n'+
          '* num_choices num_answers num_trials are integers.\n'+
          '  Their default values are %d, %d, %d respectively\n\n' % (default_choices, default_answers, default_trials) +
          'Example:\n' +
          '  python main.py 4 60 1000'
        )
        return


    total_prob = {c+1: {'score': 0.0, 'length': 0} for c in range(num_choices)}
    total_prob['random'] = {'score': 0.0, 'length': 0}

    prob_over50 = {c+1: 0 for c in range(num_choices)}
    prob_over50['random'] = 0

    print ('Number of choices:', num_choices)
    print ('Number of answers:', num_answers)
    print ('Number of trials:', num_trials)
    print ('\n')
    print ('Running Trials...')
    for i in range(num_trials):
        answers = [randint(1, num_choices) for i in range(num_answers)]
        choices = {c+1: [0] * num_answers for c in range(num_choices)}
        choices['random'] = [0] * num_answers

        for j, a in enumerate(answers):
            choices[a][j] += 1
            if a == randint(1, num_choices):
                choices['random'][j] += 1

        # print answer sheet
        if i % (num_trials/1000) == 0:
            print ('Answer Sheet:')
            print ('-' * 20)
            for i, a in enumerate(answers):
                ans = ['-' for n in range(num_choices)]
                ans[(a-1)] = 'a'
                print(i+1, '\t'+'|'.join(ans))

            print ('Probabilities:\n')
            for c in choices:
                prob = float(sum(choices[c]))/len(choices[c])
                total_prob[c]['score'] = (total_prob[c]['score']*total_prob[c]['length']+prob)/(total_prob[c]['length']+1)
                total_prob[c]['length'] += 1

                if prob >= 0.5:
                    prob_over50[c] += 1
                
                print(c, prob)

    print ('-'*20)
    print ('Average score if answering questions with:\n')
    for p in total_prob:
        print(p, total_prob[p]['score'])

    print ('\nProbabilities of scoring over 50% if answering all questions with:')
    for p in total_prob:
        print(p, prob_over50[p]/float(num_trials))

if __name__ == '__main__':
    main()
