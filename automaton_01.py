from sys import exit


def main():
    """
    決定性有限オートマトンを定義して語の判別を行う
    """
    lang_21 = Automaton_elem(
        "pqrd",  # 状態
        "ab",  # アルファベット
        [  # 動作関数
            ["p", "a", "q"],
            ["p", "b", "d"],
            ["q", "a", "q"],
            ["q", "b", "r"],
            ["r", "a", "d"],
            ["r", "b", "r"],
            ["d", "a", "d"],
            ["d", "b", "d"],
        ],
        "p",  # 初期状態
        "r",  # 受理状態
    )
    if lang_21.is_define() == 1:
        print("The automaton isn't correct.")
        exit(1)
    # print('self.states: ', lang_21.states)
    # print('self.chars: ', lang_21.chars)
    # print('self.mv_func: ', lang_21.mv_func)
    # print('self.init_state: ', lang_21.init_state)
    # print('self.acce_state: ', lang_21.acce_state)
    # print('self.now_state: ', lang_21.now_state)
    word = "aabb"
    print(">> word:", word)
    if lang_21.state_transiton(word) == 0:
        print("This word is L_21.")
    else:
        print("This word is NOT L_21.")
    print("-------------------------")
    word = "aabbaabb"
    print(">> word:", word)
    if lang_21.state_transiton(word) == 0:
        print("This word is L_21.")
    else:
        print("This word is NOT L_21.")
    print("-------------------------")
    word = "aacbb"
    print(">> word:", word)
    if lang_21.state_transiton(word) == 0:
        print("This word is L_21.")
    else:
        print("This word is NOT L_21.")
    print("-------------------------")
    return 0


class Automaton_elem:
    """
    決定性有限オートマトン
    """

    def __init__(
        self,
        state_str: str,
        char_str: str,
        mv_func_array: list,
        init_state_str: str,
        acce_state_str: str,
    ) -> None:
        """
        コンストラクタ
        """
        self.states = set(state_str)  # 状態の有限集合(Q)
        self.chars = set(char_str)  # アルファベット(Σ)
        self.mv_func = mv_func_array  # 動作関数(Q, Σ) = Q -> [Q, Σ, Q](2次元配列)
        self.init_state = init_state_str  # 初期状態(文字1つ, Qに属する)
        self.acce_state = set(acce_state_str)  # 受理状態(Qの部分集合)
        self.now_state = init_state_str  # 遷移中の状態(Qに属する)

    def init_now_state(self):
        """
        self.now_stateを初期化する
        """
        self.now_state = self.init_state  # 初期状態に戻す

    def is_define(self) -> int:
        """
        オートマトンが正しく定義されているかの確認
        正しく定義されていれば0を返す(他は1を返す)
        """
        tmp_states = []  # 状態
        tmp_chars = []  # アルファベット
        for i in self.mv_func:  # 動作関数から状態とアルファベットを取り出す
            tmp_states.append(i[0])  # Q
            tmp_chars.append(i[1])  # Σ
            tmp_states.append(i[2])  # Q
        if (
            # (受理状態 ⊆ 状態の有限集合) ∧ (初期状態 ⊆ 状態の有限集合)
            (self.acce_state <= self.states)
            and (set(self.init_state) <= self.states)
            and
            # (動作関数から取り出した状態 == 状態の有限集合) ∧ (動作関数から取り出したアルファベット == アルファベット)
            (set(tmp_states) == self.states)
            and (set(tmp_chars) == self.chars)
        ):
            return 0
        else:
            return 1

    def is_alphabet(self, txt: str):
        """
        文字列がアルファベットに属しているかを判別する
        文字列 ⊆ アルファベットであれば0を返す
        """
        if set(txt) <= self.chars:
            return 0
        else:
            return 1

    def is_accept(self) -> int:
        """
        状態遷移をさせた結果、受理状態であるかを判断する
        状態(now_state)が受理状態であれば0を返す
        """
        if set(self.now_state) <= self.acce_state:
            return 0
        else:
            return 1

    def state_transiton(self, words: str) -> int:
        """
        動作関数を用いて状態遷移を行う
        語(words)が受理可能であれば0を返す
        """
        self.init_now_state()  # 初期化
        if self.is_alphabet(words):
            return 1  # 入力文字列 <= アルファベットでない
        for w in words:  # 語を頭から順に取り出す
            for i in range(len(self.mv_func)):  # 動作関数に当てはめていく
                if (self.mv_func[i][0] == self.now_state) and (self.mv_func[i][1] == w):
                    self.now_state = self.mv_func[i][2]  # 状態遷移
                    print(
                        "({0}, {1}) = {2}".format(
                            self.mv_func[i][0], self.mv_func[i][1], self.mv_func[i][2]
                        )
                    )  # ログ
                    break
        return self.is_accept()


if __name__ == "__main__":
    main()
