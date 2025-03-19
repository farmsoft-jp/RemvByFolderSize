# ---------------------------------------------------------------------------
# フォルダ内の古いファイルを削除（上限フォルダサイズ指定）
# https://www.farmsoft.jp/
# ---------------------------------------------------------------------------
import os       # OSに依存しているさまざまな機能を利用するためのモジュール
import glob     # 引数に指定されたパターンにマッチするファイルパス名を取得
import math     # C標準で定義された数学関数へのアクセスを取得
# ---------------------------------------------------------------------------
# 設定
# ---------------------------------------------------------------------------
SIZE = 25*1024*1024*1024    # 最大フォルダサイズ（byte）
TYPES = ('*')               # 削除対象とするファイル拡張子を指定
                            # ex) TYPES = ('mp4', 'png')    ⇒ *.mp4 *.png のみ削除対象とする
                            # ex) TYPES = ('*')             ⇒ 指定なし
# ---------------------------------------------------------------------------
# フォルダサイズを算出する関数
def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total
# ---------------------------------------------------------------------------
# バイトを適切な単位に変換する関数
def convert_size(size):
    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
    i = math.floor(math.log(size, 1024)) if size > 0 else 0
    size = round(size / 1024 ** i, 2)
    return f"{size} {units[i]}"
# ---------------------------------------------------------------------------
def remv():
    PATH = os.path.dirname(__file__) + '\\'     # 本実行スクリプトの絶対パスを取得
    SCRIPTFILE = __file__                       # 本実行スクリプトの絶対パス＋ファイル名を取得
    fosize = get_dir_size(PATH)                 # フォルダサイズ算出

    # フォルダサイズが最大フォルダサイズより小さい場合は終了
    if fosize <= SIZE:
        print(f'現在のフォルダサイズは[{convert_size(fosize)}]です。')
        return
    # 削除するサイズを計算
    rsize = fosize - SIZE

    # フォルダ内にある対象拡張子のファイル一覧を取得
    files = []
    for t in TYPES:
        files += glob.glob(PATH + '*' + t)

    # ファイル名と作成日時（エポック秒）の2次元リストを作成
    # [['ファイル名', 作成日時（エポック秒）],['ファイル名', 作成日時（エポック秒）],...]
    flist = []
    for file in files:
        # 本実行スクリプトは除外
        if file == SCRIPTFILE:
            continue
        # ファイルリストに['ファイル名', 作成日時（エポック秒）]を追加
        fname = os.path.basename(file)
        ctime = os.path.getctime(file)
        flist.append([fname, ctime])

    # ファイルリストを要素２つ目の作成日時（エポック秒）で昇順ソート
    flist.sort(key=lambda x: x[1])

    # ファイルリストの作成日時（エポック秒）が古いものからファイルサイズを取得し、
    # 削除するファイルを特定
    total = 0
    lv = []
    for i in range(len(flist)):
        # フォルダは除外しファイルのみ対象
        if os.path.isfile(PATH + flist[i][0]):
            total += os.path.getsize(PATH + flist[i][0])
            lv.append(i)
            if rsize <= total:
                break
    print(f'{i+1}個のファイル（合計サイズ[{convert_size(total)}]）を削除します。')

    # 特定したファイルを削除
    for i in range(len(lv)):
        os.remove(PATH + flist[lv[i]][0])
        print(f'削除したファイル名：{flist[lv[i]][0]}')

    print(f'現在のフォルダサイズは[{convert_size(fosize-total)}]です。')
# ---------------------------------------------------------------------------
if __name__=='__main__':
    remv()
# ---------------------------------------------------------------------------
