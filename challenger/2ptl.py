from dashite import Dashite
from syouhai import Syouhai
from janken_interface import JankenInterface

class Logic(JankenInterface):

    def init(self, syoubuKaisuu):
        self.syoubuKaisuu = syoubuKaisuu
        self.history = []  # 過去の相手の手を記録する
        self.pattern_counts = {}  # パターンの出現回数を記録する辞書

    def jankenpon(self):
        if len(self.history) < 2:
            # 最初の2手はランダムで開始
            self.now_my_dashite = Dashite.GU
            return Dashite.GU

        # 直前の2手を使って次の相手の手を予測する
        prev_two_moves = tuple(self.history[-2:])
        predicted_enemy_move = self.predict_next_move(prev_two_moves)

        # 相手の次の手を予測し、それに勝つ手を選ぶ
        if predicted_enemy_move == Dashite.GU:
            self.now_my_dashite = Dashite.PA
        elif predicted_enemy_move == Dashite.CYOKI:
            self.now_my_dashite = Dashite.GU
        elif predicted_enemy_move == Dashite.PA:
            self.now_my_dashite = Dashite.CYOKI
        else:
            self.now_my_dashite = Dashite.GU  # デフォルトでグーを出す

        return self.now_my_dashite

    def kekka(self, syohai):
        # 今回の相手の手を記録
        if syohai == Syouhai.KACHI:
            if self.now_my_dashite == Dashite.GU:
                self.history.append(Dashite.CYOKI)
            elif self.now_my_dashite == Dashite.CYOKI:
                self.history.append(Dashite.PA)
            else:
                self.history.append(Dashite.GU)
        elif syohai == Syouhai.MAKE:
            if self.now_my_dashite == Dashite.GU:
                self.history.append(Dashite.PA)
            elif self.now_my_dashite == Dashite.CYOKI:
                self.history.append(Dashite.GU)
            else:
                self.history.append(Dashite.CYOKI)
        else:
            self.history.append(self.now_my_dashite)

        # 直前の3手のパターンをカウント
        if len(self.history) >= 3:
            pattern = tuple(self.history[-3:])
            if pattern in self.pattern_counts:
                self.pattern_counts[pattern] += 1
            else:
                self.pattern_counts[pattern] = 1

    def predict_next_move(self, prev_two_moves):
        # prev_two_moves + 各手の組み合わせで一番多いパターンを探す
        possible_moves = [Dashite.GU, Dashite.CYOKI, Dashite.PA]
        max_count = -1
        predicted_move = None

        for move in possible_moves:
            pattern = prev_two_moves + (move,)
            if pattern in self.pattern_counts:
                if self.pattern_counts[pattern] > max_count:
                    max_count = self.pattern_counts[pattern]
                    predicted_move = move

        return predicted_move