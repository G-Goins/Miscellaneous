import random

class LetsPlayYahtzee:
    def __init__(self):
        self.dice = [0] * 5
        self.score_sheet = {'Aces': None, 'Twos': None, 'Threes': None, 'Fours': None,
                            'Fives': None, 'Sixes': None, 'Three of a Kind': None,
                            'Four of a Kind': None, 'Full House': None, 'Small Straight': None,
                            'Large Straight': None, 'Yahtzee': None, 'Chance': None}
        self.categories = list(self.score_sheet.keys())

    def roll_dice(self, keep_i = None):
        """This will roll five dice for the game"""

        if keep_i is None:
            keep_i = []

        for i in range(5):
            if i not in keep_i:
                self.dice[i] = random.randint(1,6)
        return self.dice
    
    def score_aces(self):
        """
        Scoring methodology for Aces, if chosen
        """
        return self.dice.count(1) * 1
    
    def score_twos(self):
        """
        Scoring methodology for Twos, if chosen
        """
        return self.dice.count(2) * 2
    
    def score_threes(self):
        """
        Scoring methodology for Threes, if chosen
        """
        return self.dice.count(3) * 3
    
    def score_fours(self):
        """
        Scoring methodology for Fours, if chosen
        """
        return self.dice.count(4) * 4
    
    def score_fives(self):
        """
        Scoring methodology for Fives, if chosen
        """
        return self.dice.count(5) * 5
    
    def score_sixes(self):
        """
        Scoring methodology for Sixes, if chosen
        """
        return self.dice.count(6) * 6
    
    def score_three_of_a_kind(self):
        """
        Checks for Three of a Kind and returns the sum
        """

        if any(self.dice.count(x) >= 3 for x in set(self.dice)):
                return sum(self.dice)
        return 0
    
    def score_four_of_a_kind(self):
        """
        Checks for Four of a Kind and returns the sum
        """

        if any(self.dice.count(x) >= 4 for x in set(self.dice)):
                return sum(self.dice)
        return 0
    
    def score_full_house(self):
        """
        Returns 25 points for a Full House
        """
        counts = {x: self.dice.count(x) for x in set(self.dice)}
        if sorted(counts.values()) == [2, 3]:
            return 25
        return 0

    def score_small_straight(self):
        """
        Returns 30 points for a Small Straight
        """
        straights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        if any(straight.issubset(set(self.dice)) for straight in straights):
            return 30
        return 0
    
    def score_large_straight(self):
        """
        Returns 40 points for a Large Straight
        """
        if set(self.dice) in [{1, 2, 3, 4, 5}, {2, 3, 4, 5,6 }]:
            return 40
        return 0
    
    def score_yahtzee(self):
        """
        Returns 50 points for a Yahtzee
        """
        if len(set(self.dice)) == 1:
            return 50
        return 0
    
    def score_chance(self):
        """
        Returns the sum of all dice
        """
        return sum(self.dice)
    
    def select_category(self, category):
        """
        Selects a scoring category for the current roll
        as well as updates the score
        """
        normalized_category = category.lower().replace(" ", "_")
        method_name = 'score_' + normalized_category
        if category in self.categories:
            if self.score_sheet[category] is None:
                if hasattr(self, method_name):
                    score = getattr(self, method_name)()
                    self.score_sheet[category] = score
                    self.categories.remove(category)
                    print(f"Score for {category}: {score}")
                else:
                    print(f"No scoring method available for {category}")
            else:
                print(f"Category '{category}' already used. Pick a new one!")
        else:
            print("Invalid category")
    
    def play_turn(self):
        """
        Manages a single turn where dice can be rolled up to three times
        """
        print("Starting new turn...")
        self.roll_dice()
        print("First Roll:", self.dice)

        for i in range(2):
            keep = input("Enter indices to keep, or press enter for a re-roll: ")
            if keep.strip() == 'all':
                break
            elif keep.strip():
                keep_i = [int(k) - 1 for k in keep.split(',') if k.isdigit()]
            else:
                keep_i = []
            self.roll_dice(keep_i)
            print(f"Roll {i + 2}:", self.dice)
        
        category = ""
        while category not in self.categories:
            category = input(f"Select a category from: {', '.join(self.categories)}\n")
        self.select_category(category)

    def play_game(self):
        """
        Plays a full game of Yahtzee!
        """
        for i in range(13):
            self.play_turn()
        print("Game over. Final scores:")
        total_score = sum(score for score in self.score_sheet.values() if score is not None)
        print(self.score_sheet)
        print("Total Score:", total_score)