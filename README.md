# vistra-pj

## Trivy License Check アクション

このリポジトリには、Trivyを使用したライセンスチェックの再利用可能なGitHub Actionsカスタムアクションが含まれています。

### 使用方法

#### 1. 同じリポジトリ内から呼び出す場合

```yaml
jobs:
  check-license:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./actions/trivy-license-check
        with:
          image_name: 'my-image:latest'
```

#### 2. 他のリポジトリから呼び出す場合（anyfld/vistra-pjのポリシーを自動使用）

```yaml
jobs:
  check-license:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anyfld/vistra-pj/actions/trivy-license-check@main
        with:
          image_name: 'my-image:latest'
```
