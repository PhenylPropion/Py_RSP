from dashite import Dashite
from syouhai import Syouhai
from janken_interface import JankenInterface


class Logic(JankenInterface):

    #
    # 初回だけ呼び出される処理.
    # (10000 回のじゃんけんの最初に 1 回だけ呼び出される)
    #
    def init(self, syoubuKaisuu):

        # 勝負回数をインスタンス変数へ保存
        self.syoubuKaisuu = syoubuKaisuu

        # 直近の自分の出し手
        # ここでは変数の用意と初期化のみ
        self.now_my_dashite = None

        # 直近の敵の出し手
        # ここでは変数の用意と初期化のみ
        self.now_enemy_dashite = None

        # 敵の出し手の初期化
        self.enemy_gu_cnt = 0
        self.enemy_cyoki_cnt = 0
        self.enemy_pa_cnt = 0

        # 初回フラグ
        self.first = True

        # じゃんけんの履歴
        self.enemy_history = []
        self.my_history = []
        self.pat = 3

    def jankenpon(self):
        # 初回のみpaで出す
        if self.first:
            self.first = False
            self.second = True
            return Dashite.PA
        # 2回目はguで出す
        if self.second:
            self.second = False
            return Dashite.GU

        # パターン認識による手の予測
        if len(self.enemy_history) >= self.pat:
            recent_pattern = tuple(self.enemy_history[-self.pat:])
            predicted_enemy_move = self.predict_next_move(recent_pattern)
            self.now_my_dashite = self.counter_move(predicted_enemy_move)
            return self.now_my_dashite
        # 敵の出し手の数をカウントして
        # 一番多い出し手に対して勝てる手を
        # 出すものとする
        if self.now_enemy_dashite == Dashite.GU:
            self.enemy_gu_cnt += 1
        elif self.now_enemy_dashite == Dashite.CYOKI:
            self.enemy_cyoki_cnt += 1
        else:
            self.enemy_pa_cnt += 1

        # 敵の一番多い出し手に対して勝つ手を今回の手とする
        if self.enemy_gu_cnt >= self.enemy_cyoki_cnt:
            if self.enemy_gu_cnt >= self.enemy_pa_cnt:
                self.now_my_dashite = Dashite.PA
                return Dashite.PA
            else:
                self.now_my_dashite = Dashite.CYOKI
                return Dashite.CYOKI
        else:
            if self.enemy_cyoki_cnt >= self.enemy_pa_cnt:
                self.now_my_dashite = Dashite.GU
                return Dashite.GU
            else:
                self.now_my_dashite = Dashite.CYOKI
                return Dashite.CYOKI

    #
    # 1 回のじゃんけんに対する勝敗を受け取る.
    #
    def kekka(self, syohai):

        # 受け取った勝敗と自分の出し手により
        # 敵の出し手を判定する
        if syohai == Syouhai.KACHI:
            # 勝ちの場合
            if self.now_my_dashite == Dashite.GU:
                # 自分がグーを出した場合
                # 敵はチョキ
                self.now_enemy_dashite = Dashite.CYOKI
            elif self.now_my_dashite == Dashite.CYOKI:
                # 自分がチョキを出した場合
                # 敵はパー
                self.now_enemy_dashite = Dashite.PA
            else:
                # 自分がパーを出した場合
                # 敵はグー
                self.now_enemy_dashite = Dashite.GU

        elif syohai == Syouhai.MAKE:
            # 負けの場合

            if self.now_my_dashite == Dashite.GU:
                # 自分がグーを出した場合
                # 敵はパー
                self.now_enemy_dashite = Dashite.PA
            elif self.now_my_dashite == Dashite.CYOKI:
                # 自分がチョキを出した場合
                # 敵はグー
                self.now_enemy_dashite = Dashite.GU
            else:
                # 自分がパーを出した場合
                # 敵はチョキ
                self.now_enemy_dashite = Dashite.CYOKI
        else:
            # あいこの場合
            if self.now_my_dashite == Dashite.GU:
                # 自分がグーを出した場合
                # 敵もグー
                self.now_enemy_dashite = Dashite.GU
            elif self.now_my_dashite == Dashite.CYOKI:
                # 自分がチョキを出した場合
                # 敵もチョキ
                self.now_enemy_dashite = Dashite.CYOKI
            else:
                # 自分がパーを出した場合
                # 敵もパー
                self.now_enemy_dashite = Dashite.PA

        # 敵と自分の出し手を履歴に追加
        self.enemy_history.append(self.now_enemy_dashite)
        self.my_history.append(self.now_my_dashite)

    def predict_next_move(self, recent_pattern):
        # 履歴の中から最近のパターンに続く手を予測する
        for i in range(len(self.enemy_history) - self.pat):
            if tuple(self.enemy_history[i:i + self.pat]) == recent_pattern:
                return self.enemy_history[i + self.pat]
        return None  # パターンが見つからない場合は None を返す

    @staticmethod
    def counter_move(predicted_move):
        # 予測された敵の手に勝つ手を返す
        if predicted_move == Dashite.GU:
            return Dashite.PA
        elif predicted_move == Dashite.CYOKI:
            return Dashite.GU
        elif predicted_move == Dashite.PA:
            return Dashite.CYOKI
        else:
            return Dashite.CYOKI  # デフォルトでcykを返す
