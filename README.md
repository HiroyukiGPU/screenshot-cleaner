# SCREENSHOT CLEANER

スクリーンショットを検出して日付別に整理します。

## インストール

Python 3.10以降が必要です。macOS / Linuxを主対象にしています。

```sh
pipx install git+https://github.com/HiroyukiGPU/screenshot-cleaner.git
screenshot-cleaner --help
```

pipxを使わない場合は、仮想環境で `python -m pip install .` を実行できます。

## 使用例

```sh
screenshot-cleaner ~/Desktop
screenshot-cleaner ~/Desktop --apply
screenshot-cleaner ~/Desktop --by month --apply
```

Screenshot、Screen Shot、スクリーンショット、スクリーン ショットで始まる画像ファイルを名前で検出します。画像内容からの推測は行いません。直下のファイルを更新日別に整理し、原本を移動します。既定はプレビュー、名前衝突時は中止します。

## 開発と検証

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
```

終了コード: 通常0、検出結果ありは各コマンドの説明に従います。入力・通信・実行エラーは2、Ctrl+Cは130です。
データ保存を使うCLIは `~/.local/share/screenshot-cleaner/` に保存します。`CLI_TOOLS_DATA_HOME` で保存先の親ディレクトリを変更できます。
ネットワークサービスにはタイムアウトを設定しています。APIの制限や応答によって失敗する場合はエラーを表示します。

## ライセンス

MIT。詳しくは [LICENSE](LICENSE) を参照してください。
