# MtG_AI

[Ensemble Determinization in Monte Carlo Tree Search for the Imperfect Information Card Game Magic: The Gathering](https://ieeexplore.ieee.org/document/6218176) を基に、Magic: The Gathering にモンテカルロ木探索を導入する場合の改良手法を検討するプロジェクト

# 詳しい研究内容について

[研究発表資料](./readme.pdf)に主に記述しました。

## 概要

### 【研究背景】

デジタルカードゲームの普及により、デジタルカードゲームおよび同じゲーム性をもつトレーディングカードゲームAIの研究が進められている。
Magic: The Gatheringと呼ばれるトレーディングカードゲームAI研究ではモンテカルロ木探索が利用されており、その改良(刈り込み・シミュレーション戦略・木の構築・報酬)について研究されている。

### 【研究目的】

先行研究で行われていなかった戦闘フェイズについての改良手法を提案・検証する。

### 【研究手法】

先行研究のAIに戦闘フェイズにもモンテカルロ木探索を導入したものを実装・評価する。また、「AS」と「BS」という2手法について、先行研究で評価された改善手法と組み合わせた場合の勝率を検証する。
AS・・・アタッカー選択時にアタック可能クリーチャーを基準に木を分割し二分木として表現する手法
BS・・・ブロッカーの選択時にブロック可能クリーチャーを基準に分割する手法
基準に分割するとは、すべてのクリーチャーの行動する/しないという組み合わせを同時に探索するのではなく、
まず基準となったクリーチャーが行動する/しないといった要素を子要素とした木を探索し、探索し終わってらから次のクリーチャーの行動について探索するといった木の構築手法である。

### 【結果】AS、BSともに純粋なモンテカルロ木探索AIよりも弱い結果となった。しかし、2手法の長所と短所からよりよい改善手法の可能性が示唆された。

・モンテカルロ木探索の展開においてASを用いると更に先の手番へ探索を進めやすくなるのではないか
・ブロッカー選択時に、相手のアタッカーを基準に木を分割するとよいのではないか
・戦闘フェイズの探索時のみ負の報酬を設定するとよりよい予測ができるのではないか

# 構成

Python 3.6.5
NumPy (使用箇所は限定的なため、実装次第では不使用も可能)

# ディレクトリ構成

+---ai         : ゲームAIの実装。ルールベースプレイヤーなどが置かれている
  \-montecalro : モンテカルロ木探索AIの実装。sample系は試行用ゲームの実装
|---client     : ユーザーがMtGシミュレータを試す用のプログラム
|---deck       : ゲームで利用するカードプール・デッキリストがpythonスクリプトとして置かれている
|---games      : ゲーム本体や盤面に関わるコードが中心
  |-cards      : カードオブジェクトやカードタイプ毎のインターフェース
  \-mana       : マナ計算用のプログラム
|---main       : ゲームをプレイしたり、実験を行うためのエンドポイント
|---test       : テスト
|---util       : 汎用的なプログラムの雑多まとめ
  \-montecalro : モンテカルロ木の抽象実装。その内ここだけ分けてライブラリ化したい
|---note       : 先行研究の論文や勉強ノート
|---log        : 実験結果。 `.csv` が一番まとまっている
\---script     : 書き捨てのスクリプト系