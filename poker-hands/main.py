from time import time
import json
import poker

try:
    with open("results.json") as f:
        results = json.load(f)
except:
        results = {hand_type: 0 for hand_type in poker.Hand.get_hand_types()}

iterations = 1000000

def main():
    global iterations
    global results
    start = time()

    for i in range(iterations):
        deck = poker.Deck()
        deck.shuffle()
        results[poker.Hand(deck).get_hand_type()] += 1

    total_results = sum(results.values())

    for hand_type in poker.Hand.get_hand_types():
        print(str(hand_type).ljust(15)+"\t"+
            "%.5f%%" % (results[hand_type]/total_results * 100,)+"\t"+
            str(results[hand_type]))

    print("\nTotal Hands:\t\t"+str(total_results))

    print ("Script completed in",time()-start, "seconds.")
    with open("results.json", "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    main()